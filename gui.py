import tkinter as tk
from engine import get_response
import history

HISTORY_PATH = "chat_history.jsonl"
HISTORY_LIMIT = 200

ROOT_BG = "#f6f2ec"
USER_BUBBLE_BG = "#2c3e50"
USER_TEXT_FG = "#ffffff"
BOT_BUBBLE_BG = "#e9ded2"
BOT_TEXT_FG = "#1f1f1f"
INPUT_BG = "#ffffff"
INPUT_FG = "#1f1f1f"
ACCENT = "#b35c1e"

TYPEWRITER_DELAY_MS = 18
MAX_BUBBLE_WIDTH_RATIO = 0.66
MIN_BUBBLE_WIDTH = 220

root = tk.Tk()
root.title("Python Chatbot")
root.geometry("460x640")
root.minsize(360, 520)
root.configure(bg=ROOT_BG)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

chat_container = tk.Frame(root, bg=ROOT_BG)
chat_container.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=14, pady=14)
chat_container.grid_rowconfigure(0, weight=1)
chat_container.grid_columnconfigure(0, weight=1)

canvas = tk.Canvas(chat_container, bg=ROOT_BG, highlightthickness=0)
scrollbar = tk.Scrollbar(chat_container, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

messages_frame = tk.Frame(canvas, bg=ROOT_BG)
messages_window = canvas.create_window((0, 0), window=messages_frame, anchor="nw")

message_labels = []


def get_wraplength(canvas_width=None):
    width = canvas_width or canvas.winfo_width()
    if width <= 1:
        width = root.winfo_width()
    target = int(width * MAX_BUBBLE_WIDTH_RATIO)
    return max(MIN_BUBBLE_WIDTH, target)


def update_wraplengths(canvas_width=None):
    wrap = get_wraplength(canvas_width)
    for label in message_labels:
        label.configure(wraplength=wrap)


def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


def on_canvas_configure(event):
    canvas.itemconfig(messages_window, width=event.width)
    update_wraplengths(event.width)


messages_frame.bind("<Configure>", on_frame_configure)
canvas.bind("<Configure>", on_canvas_configure)


def scroll_to_bottom():
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)


def animate_text(label, text, index=0):
    if index > len(text):
        return
    label.configure(text=text[:index])
    label.after(TYPEWRITER_DELAY_MS, animate_text, label, text, index + 1)


def append_chat(role, message, animate=False):
    row = tk.Frame(messages_frame, bg=ROOT_BG)
    row.pack(fill=tk.X, pady=6, padx=4)

    if role == "user":
        bubble_bg = USER_BUBBLE_BG
        text_fg = USER_TEXT_FG
        justify = "right"
        side = tk.RIGHT
        anchor = "e"
    else:
        bubble_bg = BOT_BUBBLE_BG
        text_fg = BOT_TEXT_FG
        justify = "left"
        side = tk.LEFT
        anchor = "w"

    bubble = tk.Frame(row, bg=bubble_bg, padx=12, pady=8)
    bubble.pack(side=side, anchor=anchor)

    label = tk.Label(
        bubble,
        text="",
        bg=bubble_bg,
        fg=text_fg,
        justify=justify,
        wraplength=get_wraplength(),
        font=("Segoe UI", 10),
    )
    label.pack()
    message_labels.append(label)

    if animate:
        animate_text(label, message)
    else:
        label.configure(text=message)

    scroll_to_bottom()


def load_chat_history():
    entries = history.load_history(HISTORY_PATH, limit=HISTORY_LIMIT)
    for entry in entries:
        role = entry.get("role")
        message = entry.get("message", "")
        if role == "user":
            append_chat("user", message, animate=False)
        elif role == "bot":
            append_chat("bot", message, animate=False)


def send_message():
    message = chat_input.get().strip()
    if not message:
        return

    append_chat("user", message, animate=False)
    history.append_history(HISTORY_PATH, "user", message)

    bot_message = get_response(message)
    append_chat("bot", bot_message, animate=True)
    history.append_history(HISTORY_PATH, "bot", bot_message)

    chat_input.delete(0, tk.END)


chat_input = tk.Entry(root, bg=INPUT_BG, fg=INPUT_FG, relief=tk.FLAT)
chat_input.grid(row=1, column=0, sticky="ew", padx=(14, 6), pady=(0, 14), ipady=8)

send_button = tk.Button(
    root,
    text="Send",
    width=10,
    bg=ACCENT,
    fg="#ffffff",
    relief=tk.FLAT,
    command=send_message,
)
send_button.grid(row=1, column=1, sticky="e", padx=(6, 14), pady=(0, 14), ipady=4)

root.bind("<Return>", lambda event: send_message())

load_chat_history()
root.mainloop()
