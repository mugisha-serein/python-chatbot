Python Chatbot

A simple, modular, and extensible chatbot built with pure Python, Tkinter GUI, and a keyword-based intent system. Designed for learning, rapid development, and easy expansion.

Features

  Lightweight Python chatbot using pure Python (no frameworks required).
  Tkinter GUI with scrollable chat history.
  User messages on the right, bot responses on the left.
  Keyword-based intent matching (first match).

Modular design:

  knowledge.py → chatbot “brain” (intent database)
  engine.py → message processing and response logic
  gui.py → user interface
  Fallback responses for unknown input.
  Easily extensible to support new intents, NLP, or ML engines.

Architecture
  User Input → [GUI] → [Engine] → [Knowledge Base] → Response → [GUI Display]

Components:

  GUI (gui.py)
  Handles user input, display of messages, and layout.
  Modern chat-like interface using Tkinter and ScrolledText.
  Engine (engine.py)
  Cleans user input.
  Detects intent using first matched keyword strategy.
  Selects random response from intent.
  Returns fallback response if no intent matches.
  Knowledge Base (knowledge.py)
  Stores intents as a dictionary.

Each intent has:

  keywords: list of triggers
  responses: list of possible replies
  Includes "unknown" intent for fallback.

Project Structure
python-chatbot/
│
├─ gui.py               # Tkinter GUI
├─ engine.py            # Chatbot logic and intent matching
├─ knowledge.py         # Intent database
└─ README.md            # Project documentation
Setup & Installation

Clone repository:

  git clone <your-repo-url>
  cd python-chatbot

Note: Tkinter comes with most Python installations. For Docker, see Dockerfile instructions.

Run the chatbot:
python gui.py

Usage

  Type a message in the input box.
  Press Enter or click Send.
  Chatbot will display responses in the scrollable chat area.

How it Works

  User input is captured by Tkinter.
  Engine calls clean_message() to normalize text.
  detect_intent() loops through all intents except "unknown":
  If a keyword matches first occurrence, returns that intent.
  If no match → "unknown" intent.
  select_response() picks a random response for the detected intent.
  Bot response is displayed in the chat GUI.

Note: The chatbot currently uses first matched keyword logic. This makes it simple, predictable, and easy to expand.

Future Updates & Expansion

Planned enhancements:

  Add more intents: e.g., time, date, jokes, weather.
  Advanced NLP: integrate simple machine learning or transformer models.
  Context awareness: allow multi-turn conversation.
  Persistent knowledge: save conversation history or user preferences.

GUI improvements:

  User chat aligned to right, bot chat aligned to left
  Modern color scheme and animations
  Responsive resizing and scrollable history

Docker improvements:

  GUI support in Linux containers
  Headless mode for testing
  Contributing
  Fork the repository
  Add new intents to knowledge.py
  Extend engine.py for new logic
  Update GUI in gui.py if needed
  Submit pull request

License
You are free to use, modify, and distribute for personal or educational purposes.
