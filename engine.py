import random
from datetime import datetime
import knowledge


def clean_message(message):
    message =  message.strip().lower()
    return message


def detect_intent(message):
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


def select_response(intent_name):
    if intent_name is None:
        intent_name = "unknown"
        
    responses = knowledge.INTENTS[intent_name]["responses"]
    return random.choice(responses) 


def get_response(message):
    """
    The main function called by GUI.
    """
    cleaned = clean_message(message)
    intent = detect_intent(cleaned)
    if intent == "time":
        now = datetime.now()
        return now.strftime("Current time is %I:%M %p.")
    if intent == "date":
        today = datetime.now()
        return today.strftime("Today's date is %B %d, %Y.")

    response = select_response(intent)
    return response
