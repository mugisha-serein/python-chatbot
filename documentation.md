# Documentation Update

## Feature: Conversation History
The chat now persists conversation history across sessions using a simple JSON Lines file stored in the project root.

## Added
- `history.py` for loading, appending, and clearing chat history.
- `chat_history.jsonl` runtime file created on first message send.
- History loading on app startup (last 200 messages).

## Updated
- `gui.py` loads history on startup.
- `gui.py` appends user/bot messages to history after each exchange.
- `gui.py` centralizes chat display via `append_chat()`.

## Removed
- None.
