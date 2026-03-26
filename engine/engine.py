import random
import re
from datetime import datetime
from typing import Dict, List, Optional
from .advanced_nlp import AdvancedNLPEngine

import knowledge
import requests
from requests.exceptions import RequestException


GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_CODE_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Light rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Light snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Rain showers",
    81: "Heavy rain showers",
    82: "Violent rain showers",
    85: "Light snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def clean_message(message: str) -> str:
    return message.strip().lower()


def extract_weather_location(message: str) -> Optional[str]:
    stopwords = ["today", "tomorrow", "tonight", "now", "please", "please?", "thanks"]
    if " in " in message:
        _, location = message.split(" in ", 1)
    elif " for " in message:
        _, location = message.split(" for ", 1)
    else:
        location = message

    for stopword in stopwords:
        location = re.split(r"\b" + re.escape(stopword) + r"\b", location)[0]

    location = re.sub(r"\b(weather|forecast|temperature)\b", "", location)
    return location.strip() or None


def geocode_location(query: str) -> Optional[Dict[str, str]]:
    try:
        response = requests.get(
            GEOCODE_URL,
            params={"name": query, "count": 1, "language": "en", "format": "json"},
            timeout=6,
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results") or []
        if not results:
            return None
        return results[0]
    except RequestException:
        return None


def fetch_current_weather(lat: float, lon: float, timezone: str = "auto") -> Optional[Dict[str, float]]:
    try:
        response = requests.get(
            WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": True,
                "timezone": timezone,
            },
            timeout=6,
        )
        response.raise_for_status()
        return response.json().get("current_weather")
    except RequestException:
        return None


def format_location_label(place: Dict[str, str]) -> str:
    parts = [place.get("name"), place.get("admin1"), place.get("country")]
    return ", ".join([part for part in parts if part])


def build_weather_response(location_query: str) -> str:
    place = geocode_location(location_query)
    if not place:
        return f"I couldn't find a location called '{location_query}'. Please try a nearby city."

    latitude = place.get("latitude")
    longitude = place.get("longitude")
    if latitude is None or longitude is None:
        return "I couldn't determine coordinates for that location."

    weather = fetch_current_weather(
        latitude,
        longitude,
        timezone=place.get("timezone", "auto"),
    )
    if not weather:
        return "I couldn't retrieve live weather right now. Please try again shortly."

    description = WEATHER_CODE_DESCRIPTIONS.get(weather.get("weathercode"), "current conditions")
    location_label = format_location_label(place) or location_query.title()
    temperature = weather.get("temperature")
    wind_speed = weather.get("windspeed")
    wind_direction = weather.get("winddirection")
    temperature_text = f"{temperature:.1f} degrees C" if temperature is not None else "an unknown temperature"
    wind_text = f"windspeed {wind_speed:.1f} m/s" if wind_speed is not None else "wind data unavailable"
    direction_text = f" at {wind_direction:.0f} degrees" if wind_direction is not None else ""

    return (
        f"Live weather in {location_label}: {description.lower()}, {temperature_text}, {wind_text}{direction_text}."
    )


def get_time_response() -> str:
    now = datetime.now()
    return now.strftime("Current time is %I:%M %p.")


def get_date_response() -> str:
    today = datetime.now()
    return today.strftime("Today's date is %B %d, %Y.")


class RuleEngine:
    def detect_intent(self, message: str) -> Optional[str]:
        intent_order = getattr(knowledge, "INTENT_PRIORITY", [])
        ordered_intents = []
        seen = set()

        for intent_name in intent_order:
            if intent_name in knowledge.INTENTS and intent_name != "unknown" and intent_name not in seen:
                ordered_intents.append(intent_name)
                seen.add(intent_name)

        for intent_name in knowledge.INTENTS.keys():
            if intent_name != "unknown" and intent_name not in seen:
                ordered_intents.append(intent_name)
                seen.add(intent_name)

        for intent_name in ordered_intents:
            intent_data = knowledge.INTENTS[intent_name]
            keywords = intent_data.get("keywords", [])
            for keyword in keywords:
                if keyword in message:
                    return intent_name

        return None

    def select_response(self, intent_name: Optional[str]) -> str:
        if intent_name is None:
            intent_name = "unknown"

        responses = knowledge.INTENTS.get(intent_name, knowledge.INTENTS["unknown"])["responses"]
        return random.choice(responses)


class NLPEngine:
    FALLBACK_INTENT = "unknown"

    def __init__(self):
        self.advanced = AdvancedNLPEngine()

    def classify_intent(self, message: str, context: List[Dict[str, str]]) -> Optional[str]:
        advanced = self.advanced.classify_intent(message)
        if advanced and advanced["score"] >= self.advanced.threshold:
            return advanced["intent"]

        keywords = {
            "help": ["assist", "help", "support"],
            "weather": ["weather", "forecast", "temperature", "rain", "sunny"],
            "greeting": ["hey", "hello", "hi"],
            "goodbye": ["bye", "goodbye", "see you"],
            "thanks": ["thank", "thanks"],
        }

        tokens = set(message.split())
        for intent, candidates in keywords.items():
            if tokens.intersection(candidates):
                return intent

        recent_user = [entry for entry in context if entry.get("role") == "user"]
        if recent_user and "remind" in recent_user[-1].get("message", ""):
            return "reminder"

        return None


class DecisionEngine:
    def __init__(self, rule_engine: RuleEngine):
        self.rule_engine = rule_engine

    def resolve_intent(self, rule_intent: Optional[str], nlp_intent: Optional[str]) -> str:
        if rule_intent:
            return rule_intent
        if nlp_intent:
            return nlp_intent
        return "unknown"

    def choose_response(
        self,
        intent: str,
        message: str,
        context: List[Dict[str, str]],
    ) -> str:
        if intent == "time":
            return get_time_response()

        if intent == "date":
            return get_date_response()

        if intent == "weather":
            location_query = extract_weather_location(message)
            if not location_query:
                return self.rule_engine.select_response("weather")
            return build_weather_response(location_query)

        return self.rule_engine.select_response(intent)


class Engine:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.nlp_engine = NLPEngine()
        self.decision_engine = DecisionEngine(self.rule_engine)

    def respond(self, message: str, context: Optional[List[Dict[str, str]]] = None) -> str:
        cleaned = clean_message(message)
        context = context or []
        rule_intent = self.rule_engine.detect_intent(cleaned)
        nlp_intent = self.nlp_engine.classify_intent(cleaned, context)
        intent = self.decision_engine.resolve_intent(rule_intent, nlp_intent)
        return self.decision_engine.choose_response(intent, cleaned, context)


hybrid_engine = Engine()
