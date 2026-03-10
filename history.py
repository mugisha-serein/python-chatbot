import json
from datetime import datetime
from pathlib import Path


def load_history(path, limit=None):
    history_path = Path(path)
    if not history_path.exists():
        return []

    entries = []
    with history_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            entries.append(entry)

    if limit is not None:
        entries = entries[-limit:]

    return entries


def append_history(path, role, message, timestamp=None):
    entry = {
        "ts": timestamp or datetime.now().isoformat(timespec="seconds"),
        "role": role,
        "message": message,
    }
    with open(path, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=True) + "\n")
    return entry


def clear_history(path):
    history_path = Path(path)
    if history_path.exists():
        history_path.unlink()
