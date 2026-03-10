import tkinter as tk
from tkinter import scrolledtext
from engine import get_response
import history


root = tk.Tk()
root.title("Python Chatbot")
root.geometry("400x600")

HISTORY_PATH = "chat_history.jsonl"
HISTORY_LIMIT = 200

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_input = tk.Entry(root, width=40)
chat_input.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X, expand=True)

def append_chat(prefix, message):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"{prefix}: {message}\n")
    chat_area.config(state='disabled')
    chat_area.see(tk.END)

def load_chat_history():
    entries = history.load_history(HISTORY_PATH, limit=HISTORY_LIMIT)
    for entry in entries:
        role = entry.get("role")
        message = entry.get("message", "")
        if role == "user":
            append_chat("You", message)
        elif role == "bot":
            append_chat("Bot", message)

def send_message():
    message = chat_input.get().strip()
    if message:
        append_chat("You", message)
        history.append_history(HISTORY_PATH, "user", message)

        bot_message = get_response(message)
        append_chat("Bot", bot_message)
        history.append_history(HISTORY_PATH, "bot", bot_message)

        chat_input.delete(0, tk.END)

send_button = tk.Button(root, text="Send", width=10, command=send_message)
send_button.pack(padx=10, pady=10)

root.bind('<Return>', lambda event: send_message())

load_chat_history()
root.mainloop()
