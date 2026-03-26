import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import psycopg2
    import psycopg2.extras
except ImportError:  # pragma: no cover
    psycopg2 = None

try:
    import redis
except ImportError:  # pragma: no cover
    redis = None

from . import history

DEFAULT_HISTORY_PATH = "chat_history.jsonl"
DEFAULT_PREFERENCES_PATH = "user_preferences.json"


class CacheEntry:
    def __init__(self, value: Any, expires_at: Optional[float]):
        self.value = value
        self.expires_at = expires_at

    def is_valid(self) -> bool:
        return self.expires_at is None or time.time() < self.expires_at


class InMemoryCache:
    def __init__(self):
        self._store: Dict[str, CacheEntry] = {}

    def get(self, key: str) -> Any:
        entry = self._store.get(key)
        if not entry:
            return None
        if entry.is_valid():
            return entry.value
        self._store.pop(key, None)
        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        expires_at = None if ttl is None else time.time() + ttl
        self._store[key] = CacheEntry(value, expires_at)

    def clear(self) -> None:
        self._store.clear()


class DataLayer:
    def __init__(
        self,
        history_path: str = DEFAULT_HISTORY_PATH,
        preferences_path: str = DEFAULT_PREFERENCES_PATH,
        postgres_dsn: Optional[str] = None,
        redis_url: Optional[str] = None,
    ):
        self.history_path = Path(history_path)
        self.preferences_path = Path(preferences_path)
        self.cache = InMemoryCache()
        self._postgres_dsn = postgres_dsn or os.environ.get("CHATBOT_POSTGRES_DSN")
        self._redis_url = redis_url or os.environ.get("CHATBOT_REDIS_URL")
        self._pg_conn = self._connect_postgres()
        self._redis_client = self._connect_redis()

    def _connect_postgres(self):
        if not self._postgres_dsn or psycopg2 is None:
            return None
        try:
            conn = psycopg2.connect(self._postgres_dsn, connect_timeout=5)
            conn.autocommit = False
            self._ensure_schema(conn)
            return conn
        except Exception:
            return None

    def _ensure_schema(self, conn):
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    ts TIMESTAMPTZ NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_preferences (
                    key TEXT PRIMARY KEY,
                    value JSONB NOT NULL
                )
                """
            )
        conn.commit()

    def _connect_redis(self):
        if not self._redis_url or redis is None:
            return None
        try:
            return redis.from_url(self._redis_url, socket_timeout=5)
        except Exception:
            return None

    def _insert_history_pg(self, entry: Dict[str, Any]) -> None:
        if not self._pg_conn:
            return
        try:
            with self._pg_conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO chat_history (ts, role, message) VALUES (%s, %s, %s)",
                    (entry["ts"], entry["role"], entry["message"]),
                )
            self._pg_conn.commit()
        except Exception:
            self._pg_conn.rollback()

    def _save_preferences_pg(self, prefs: Dict[str, Any]) -> None:
        if not self._pg_conn:
            return
        try:
            json_payload = json.dumps(prefs)
            with self._pg_conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO user_preferences (key, value)
                    VALUES (%s, %s::jsonb)
                    ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value
                    """,
                    ("default", json_payload),
                )
            self._pg_conn.commit()
        except Exception:
            self._pg_conn.rollback()

    def _load_preferences_pg(self) -> Optional[Dict[str, Any]]:
        if not self._pg_conn:
            return None
        try:
            with self._pg_conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute("SELECT value FROM user_preferences WHERE key = %s", ("default",))
                row = cursor.fetchone()
                if row and row.get("value"):
                    return row["value"]
        except Exception:
            self._pg_conn.rollback()
        return None

    def _context_key(self, session_id: str) -> str:
        return f"context:{session_id}"

    # History helpers
    def load_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        return history.load_history(self.history_path, limit=limit)

    def append_history(self, role: str, message: str, timestamp: Optional[str] = None) -> Dict[str, Any]:
        entry = history.append_history(self.history_path, role, message, timestamp)
        self._insert_history_pg(entry)
        return entry

    # Preferences helpers
    def load_preferences(self) -> Dict[str, Any]:
        from preferences import load_preferences

        prefs = load_preferences(self.preferences_path)
        pg_prefs = self._load_preferences_pg()
        if isinstance(pg_prefs, dict):
            prefs.update({k: v for k, v in pg_prefs.items() if k in prefs})
        return prefs

    def save_preferences(self, prefs: Dict[str, Any]) -> None:
        from preferences import save_preferences

        save_preferences(prefs, self.preferences_path)
        self._save_preferences_pg(prefs)

    # Cache helpers
    def get_cached(self, key: str) -> Any:
        return self.cache.get(key)

    def set_cached(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        self.cache.set(key, value, ttl)

    def clear_cache(self) -> None:
        self.cache.clear()

    # Context helpers
    def load_context(self, session_id: str) -> List[Dict[str, str]]:
        key = self._context_key(session_id)
        if self._redis_client:
            try:
                raw = self._redis_client.get(key)
                if raw:
                    return json.loads(raw)
            except Exception:
                pass
        cached = self.get_cached(key)
        if isinstance(cached, list):
            return cached
        return []

    def save_context(self, session_id: str, context: List[Dict[str, str]], ttl: Optional[int] = None) -> None:
        key = self._context_key(session_id)
        payload = json.dumps(context)
        if self._redis_client:
            try:
                self._redis_client.set(key, payload, ex=ttl)
                return
            except Exception:
                pass
        self.set_cached(key, context, ttl=ttl)
