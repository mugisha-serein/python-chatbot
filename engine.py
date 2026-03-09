import random
import knowledge


def clean_message(message):
    message =  message.strip().lower()
    return message


def detect_intent(message):
    for intent_name, intent_data in knowledge.INTENTS.items():
        if intent_name == "unknown":
            continue
        
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
    response = select_response(intent)
    return response