import re
from datetime import datetime
from typing import Optional


def clean_text(message: str) -> str:
    "Normalize raw text for intent detection."
    return message.strip().lower()


def extract_weather_location(message: str) -> Optional[str]:
    "Try to isolate the location portion from a weather request."
    stopwords = ["today", "tomorrow", "tonight", "now", "please", "thanks"]
    lower_message = message.lower()
    if " in " in lower_message:
        _, location = lower_message.split(" in ", 1)
    elif " for " in lower_message:
        _, location = lower_message.split(" for ", 1)
    else:
        location = lower_message

    for stopword in stopwords:
        location = re.split(r'\b' + re.escape(stopword) + r'\b', location)[0]

    location = re.sub(r'\b(weather|forecast|temperature)\b', "", location)
    return location.strip() or None


def get_time_response() -> str:
    now = datetime.now()
    return now.strftime("Current time is %I:%M %p.")


def get_date_response() -> str:
    today = datetime.now()
    return today.strftime("Today's date is %B %d, %Y.")