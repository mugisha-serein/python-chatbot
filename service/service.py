from typing import List, Optional

import preferences
from engine import clean_message, extract_weather_location, hybrid_engine

from data import DataLayer


class ChatService:
    DEFAULT_SESSION = "default"
    CONTEXT_WINDOW = 24
    CONTEXT_TTL = 1800
    SECURITY_BLOCKLIST = {"drop table", "delete database", "shutdown", "malware", "hack"}

    def __init__(self, data_layer: Optional[DataLayer] = None, weather_cache_ttl: int = 600):
        self.data_layer = data_layer or DataLayer()
        self.weather_cache_ttl = weather_cache_ttl

    def process_message(self, raw_message: str, session_id: Optional[str] = None) -> str:
        message = self.receive_input(raw_message)
        if not self.validate_input(message):
            return ""

        session = session_id or self.DEFAULT_SESSION
        context = self.load_user_context(session)
        cleaned = self.clean_text(message)

        preference_response = preferences.handle_message(
            cleaned,
            loader=self.data_layer.load_preferences,
            saver=self.data_layer.save_preferences,
        )
        if preference_response:
            response = preference_response
        else:
            intent = self.detect_intent(cleaned)
            strategy = self.choose_response_strategy(intent)
            response = self.generate_response(strategy, cleaned, context)

        self.store_message(session, message, response, context)
        return self.personalize_response(response)

    def receive_input(self, message: str) -> str:
        return message or ""

    def validate_input(self, message: str) -> bool:
        cleaned = message.strip()
        if not cleaned:
            return False
        return self.security_check(cleaned)

    def load_user_context(self, session_id: str) -> List[dict]:
        return self.data_layer.load_context(session_id)

    def clean_text(self, message: str) -> str:
        return clean_message(message)

    def detect_intent(self, cleaned: str) -> str:
        intent = hybrid_engine.rule_engine.detect_intent(cleaned)
        if intent:
            return intent
        return "unknown"

    def choose_response_strategy(self, intent: str) -> str:
        return intent

    def generate_response(self, strategy: str, cleaned: str, context: List[dict]) -> str:
        cache_key = self.build_weather_cache_key(cleaned) if strategy == "weather" else None
        if cache_key:
            cached = self.data_layer.get_cached(cache_key)
            if cached:
                return cached
        response = hybrid_engine.decision_engine.choose_response(strategy, cleaned, context)
        if cache_key:
            self.data_layer.set_cached(cache_key, response, ttl=self.weather_cache_ttl)
        return response

    def store_message(self, session_id: str, user_message: str, bot_response: str, context: List[dict]) -> None:
        self.data_layer.append_history("user", user_message)
        if bot_response:
            self.data_layer.append_history("bot", bot_response)
        self.update_context(session_id, user_message, bot_response, context)

    def personalize_response(self, response: str) -> str:
        prefs = self.data_layer.load_preferences()
        name = prefs.get("name")
        if name and name.lower() not in response.lower():
            return f"{response} (remembering you as {name})."
        return response

    def security_check(self, message: str) -> bool:
        lower = message.lower()
        return all(block not in lower for block in self.SECURITY_BLOCKLIST)

    def update_context(self, session_id: str, user_message: str, bot_response: str, context: List[dict]) -> None:
        context.append({"role": "user", "message": user_message})
        context.append({"role": "bot", "message": bot_response})
        trimmed = context[-self.CONTEXT_WINDOW :]
        self.data_layer.save_context(session_id, trimmed, ttl=self.CONTEXT_TTL)

    def build_weather_cache_key(self, message: str) -> Optional[str]:
        trigger_terms = ("weather", "forecast", "temperature")
        if not any(term in message for term in trigger_terms):
            return None
        location_query = extract_weather_location(message)
        if not location_query:
            return None
        return f"weather:{location_query.lower()}"
