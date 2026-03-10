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

    "time": {
        "keywords": ["time", "current time", "what time is it"],
        "responses": [
            "Checking the time..."
        ],
    },

    "date": {
        "keywords": ["date", "today's date", "what date is it"],
        "responses": [
            "Checking today's date..."
        ],
    },

    "joke": {
        "keywords": ["joke", "make me laugh", "funny"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "I told my computer I needed a break, and it said: 'No problem, I'll go to sleep.'",
            "Why was the developer unhappy at their job? They wanted arrays.",
            "I would tell you a UDP joke, but you might not get it."
        ],
    },

    "weather": {
        "keywords": ["weather", "forecast", "temperature"],
        "responses": [
            "I can't access live weather yet. Tell me your city and I can offer general tips.",
            "I don't have live weather data right now, but I can help you think through what to wear."
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
