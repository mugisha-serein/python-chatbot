import json
import re
from pathlib import Path

PREFERENCES_PATH = "user_preferences.json"


def _default_preferences():
    return {
        "name": None,
        "favorites": {},
        "likes": [],
        "preferences": [],
    }


def load_preferences(path=PREFERENCES_PATH):
    pref_path = Path(path)
    if not pref_path.exists():
        return _default_preferences()
    try:
        with pref_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except json.JSONDecodeError:
        return _default_preferences()

    prefs = _default_preferences()
    prefs.update({k: v for k, v in data.items() if k in prefs})
    return prefs


def save_preferences(prefs, path=PREFERENCES_PATH):
    pref_path = Path(path)
    with pref_path.open("w", encoding="utf-8") as handle:
        json.dump(prefs, handle, ensure_ascii=True, indent=2)


def _clean_value(value):
    return value.strip().strip(".!?")


def _normalize_list_value(value):
    return re.sub(r"\s+", " ", value.strip())


def _add_unique(values, item):
    normalized = item.lower()
    if all(existing.lower() != normalized for existing in values):
        values.append(item)


def _summarize_preferences(prefs):
    parts = []
    if prefs.get("name"):
        parts.append(f"Your name is {prefs['name']}.")
    if prefs.get("favorites"):
        favorite_parts = []
        for category, value in prefs["favorites"].items():
            label = category if category != "general" else "favorite"
            favorite_parts.append(f"{label}: {value}")
        parts.append("Favorites: " + ", ".join(favorite_parts) + ".")
    if prefs.get("likes"):
        parts.append("Likes: " + ", ".join(prefs["likes"]) + ".")
    if prefs.get("preferences"):
        parts.append("Preferences: " + ", ".join(prefs["preferences"]) + ".")
    return " ".join(parts).strip()


def handle_message(message, loader=None, saver=None):
    loader = loader or load_preferences
    saver = saver or save_preferences
    prefs = loader()

    if re.search(r"\bwhat(?:'s| is) my name\b", message):
        name = prefs.get("name")
        return f"Your name is {name}." if name else "I don't know your name yet."

    favorite_match = re.search(r"\bwhat(?:'s| is) my favou?rite ([a-z ]+)\b", message)
    if favorite_match:
        category = favorite_match.group(1).strip()
        value = prefs.get("favorites", {}).get(category)
        if value:
            return f"Your favorite {category} is {value}."
        return f"I don't know your favorite {category} yet."

    if re.search(r"\bwhat(?:'s| is) my favou?rite\b", message):
        value = prefs.get("favorites", {}).get("general")
        return f"Your favorite is {value}." if value else "I don't know your favorite yet."

    if re.search(r"\bwhat do i (?:like|love)\b", message):
        likes = prefs.get("likes", [])
        if likes:
            return "You like " + ", ".join(likes) + "."
        return "I don't know what you like yet."

    if re.search(r"\bwhat do i prefer\b", message) or re.search(r"\bwhat are my preferences\b", message):
        preferences = prefs.get("preferences", [])
        if preferences:
            return "You prefer " + ", ".join(preferences) + "."
        return "I don't know your preferences yet."

    if re.search(r"\bwhat do you remember about me\b", message) or re.search(
        r"\bwhat do you know about me\b", message
    ):
        summary = _summarize_preferences(prefs)
        return summary if summary else "I don't have any saved preferences yet."

    name_match = re.search(r"\bmy name is (.+)", message)
    if not name_match:
        name_match = re.search(r"\bcall me (.+)", message)
    if name_match:
        name = _clean_value(name_match.group(1))
        prefs["name"] = name
        saver(prefs)
        return f"Got it. I'll remember your name is {name}."

    favorite_match = re.search(r"\bmy favou?rite ([a-z ]+?) is (.+)", message)
    if favorite_match:
        category = _normalize_list_value(favorite_match.group(1).strip())
        value = _clean_value(favorite_match.group(2))
        prefs.setdefault("favorites", {})[category] = value
        saver(prefs)
        return f"Got it. I'll remember your favorite {category} is {value}."

    favorite_match = re.search(r"\bmy favou?rite is (.+)", message)
    if favorite_match:
        value = _clean_value(favorite_match.group(1))
        prefs.setdefault("favorites", {})["general"] = value
        saver(prefs)
        return f"Got it. I'll remember your favorite is {value}."

    like_match = re.search(r"\bi (?:really )?(like|love|prefer) (.+)", message)
    if like_match:
        verb = like_match.group(1)
        value = _normalize_list_value(_clean_value(like_match.group(2)))
        if verb == "prefer":
            prefs.setdefault("preferences", [])
            _add_unique(prefs["preferences"], value)
        else:
            prefs.setdefault("likes", [])
            _add_unique(prefs["likes"], value)
        saver(prefs)
        return f"Thanks. I'll remember you {verb} {value}."

    return None
