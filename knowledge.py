INTENTS = {
    "greeting": {
        "keywords": ["hi", "hello", "hey"],
        "responses": [
            "Hello! How can I assist you today?", 
            "Hi there! What can I do for you?",
            "Hi!"
        ],
    },
    
    "goodbye": {
        "keywords": ["bye", "goodbye", "see you later"],
        "responses": [
            "Goodbye!", 
            "See you!", 
            "Take care!"
        ],
    },
    
    "thanks": {
        "keywords": ["thanks", "thank you", "thx"],
        "responses": [
            "You're welcome!", 
            "No problem!", 
            "My pleasure!",
            "Happy to help!"
        ],
    },
    
    "help": {
        "keywords": ["help", "assist", "i need help"],
        "responses": [
            "I can answer simple questions and have basic conversations. What would you like to talk about?",
            "I'd be happy to help you!", 
            "What do you need assistance with?",
            "I'm still a simple chatbot, but I'll do my best to assist you!"
        ],
    },
    
    "unknown": {
        "responses": [
            "I'm not sure I understand. Can you rephrase that?", 
            "Sorry, I don't know how to respond to that.", 
            "Can you try asking in a different way?"
        ],
    },
}