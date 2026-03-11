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

    "capabilities": {
        "keywords": ["what can you do", "your capabilities", "what are your features", "what do you do"],
        "responses": [
            "I can handle simple questions, small talk, facts, and basic reminders. Try asking for the time or a joke.",
            "I support keyword-based intents like time, date, jokes, facts, and small talk.",
            "I can do simple conversations, quick facts, and lightweight help. Ask me something!"
        ],
    },

    "identity": {
        "keywords": ["who are you", "what are you", "your name", "what's your name", "what is your name"],
        "responses": [
            "I'm a simple Python chatbot built around keyword intents.",
            "I'm a lightweight chatbot demo written in Python.",
            "I'm your friendly local chatbot, running on a small intent system."
        ],
    },

    "creator": {
        "keywords": ["who made you", "who created you", "your creator", "who built you"],
        "responses": [
            "I was built as a small Python chatbot project.",
            "I'm a demo bot created by Mugisha Serein for learning and experimentation.",
            "A developer put me together as a lightweight Python chatbot."
        ],
    },

    "smalltalk_howareyou": {
        "keywords": ["how are you", "how's it going", "how are things", "how do you do", "what's up"],
        "responses": [
            "I'm doing well, thanks! How are you?",
            "All good on my end. How can I help?",
            "Feeling helpful today. What can I do for you?"
        ],
    },

    "smalltalk_mood": {
        "keywords": ["i'm bored", "im bored", "i am bored", "i feel bored", "i'm tired", "im tired", "i am tired"],
        "responses": [
            "Want a quick joke or a fun fact to pass the time?",
            "I can share a joke, a fact, or help you plan a small task.",
            "I can help you find something quick to do. Want a fun fact?"
        ],
    },

    "fact": {
        "keywords": ["fact", "fun fact", "random fact", "tell me a fact"],
        "responses": [
            "Octopuses have three hearts.",
            "A day on Venus is longer than its year.",
            "Honey can stay edible for a very long time thanks to its low moisture and acidity.",
            "Light from the Sun takes about 8 minutes to reach Earth.",
            "There are 8 planets in our solar system."
        ],
    },

    "reminder": {
        "keywords": ["remind me", "set a reminder", "reminder"],
        "responses": [
            "I can't set reminders yet, but if you tell me the task and time, I can format it for you.",
            "Reminders aren't supported yet. Want me to draft a checklist instead?",
            "I don't have a reminder system yet, but I can help you plan what to do next."
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
