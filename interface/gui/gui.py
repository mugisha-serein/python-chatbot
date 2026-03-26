import sys
import random
from pathlib import Path
import threading
from typing import Optional

sys.path.append(str(Path(__file__).resolve().parents[2]))

import tkinter as tk
from controller.controller import default_controller

try:
    import speech_recognition as sr
except ImportError:
    sr = None

HISTORY_LIMIT = 200

ROOT_BG = '#f6f2ec'
USER_BUBBLE_BG = '#2c3e50'
USER_TEXT_FG = '#ffffff'
BOT_BUBBLE_BG = '#e9ded2'
BOT_TEXT_FG = '#1f1f1f'
INPUT_BG = '#ffffff'
INPUT_FG = '#1f1f1f'
ACCENT = '#b35c1e'

TYPEWRITER_DELAY_MS = 18
MAX_BUBBLE_WIDTH_RATIO = 0.66
MIN_BUBBLE_WIDTH = 220
WAVE_CANVAS_HEIGHT = 48

VOICE_ICON = 'Mic'
VOICE_LISTENING_LABEL = 'Listening...'
VOICE_TIMEOUT = 6
VOICE_PHRASE_LIMIT = 12
VOICE_UNAVAILABLE_MESSAGE = 'Voice chat requires the speech_recognition package and a microphone.'
VOICE_ERROR_TEMPLATE = 'Voice chat: {}'

root = tk.Tk()
root.title('Python Chatbot')
root.geometry('460x640')
root.minsize(360, 520)
root.configure(bg=ROOT_BG)

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)
root.grid_columnconfigure(2, weight=0)
root.grid_rowconfigure(2, weight=0)

chat_container = tk.Frame(root, bg=ROOT_BG)
chat_container.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=14, pady=14)
chat_container.grid_rowconfigure(0, weight=1)
chat_container.grid_columnconfigure(0, weight=1)

canvas = tk.Canvas(chat_container, bg=ROOT_BG, highlightthickness=0)
scrollbar = tk.Scrollbar(chat_container, orient='vertical', command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

canvas.grid(row=0, column=0, sticky='nsew')
scrollbar.grid(row=0, column=1, sticky='ns')

messages_frame = tk.Frame(canvas, bg=ROOT_BG)
messages_window = canvas.create_window((0, 0), window=messages_frame, anchor='nw')

message_labels = []
voice_button: Optional[tk.Button] = None
wave_visualizer = None


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
    canvas.configure(scrollregion=canvas.bbox('all'))


def on_canvas_configure(event):
    canvas.itemconfig(messages_window, width=event.width)
    update_wraplengths(event.width)


messages_frame.bind('<Configure>', on_frame_configure)
canvas.bind('<Configure>', on_canvas_configure)


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

    if role == 'user':
        bubble_bg = USER_BUBBLE_BG
        text_fg = USER_TEXT_FG
        justify = 'right'
        side = tk.RIGHT
        anchor = 'e'
    else:
        bubble_bg = BOT_BUBBLE_BG
        text_fg = BOT_TEXT_FG
        justify = 'left'
        side = tk.LEFT
        anchor = 'w'

    bubble = tk.Frame(row, bg=bubble_bg, padx=12, pady=8)
    bubble.pack(side=side, anchor=anchor)

    label = tk.Label(
        bubble,
        text='',
        bg=bubble_bg,
        fg=text_fg,
        justify=justify,
        wraplength=get_wraplength(),
        font=('Segoe UI', 10),
    )
    label.pack()
    message_labels.append(label)

    if animate:
        animate_text(label, message)
    else:
        label.configure(text=message)

    scroll_to_bottom()


def _set_voice_button_state(text: Optional[str] = None, state: str = 'normal'):
    if voice_button:
        voice_button.config(text=text or VOICE_ICON, state=state)


def _notify_voice_issue(message: str):
    root.after(0, lambda: append_chat('bot', message))


def _reset_voice_button():
    _set_voice_button_state(state='normal')
    if wave_visualizer:
        wave_visualizer.hide()

class WaveVisualizer:
    BAR_MIN_HEIGHT = 10
    BAR_MAX_HEIGHT = WAVE_CANVAS_HEIGHT - 8
    ANIMATION_INTERVAL = 90

    def __init__(self, frame, canvas, bar_width=10, bar_gap=6):
        self.frame = frame
        self.canvas = canvas
        self.bar_width = bar_width
        self.bar_gap = bar_gap
        self.bars = []
        self.animation_id = None
        self.running = False
        self.canvas.bind('<Configure>', self._on_configure)

    def show(self):
        if self.running:
            return
        self.frame.grid()
        self.running = True
        self._redraw_bars()
        self._animate()

    def hide(self):
        self.running = False
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
            self.animation_id = None
        self.canvas.delete('bar')
        self.bars = []
        self.frame.grid_remove()

    def _on_configure(self, event):
        if self.running:
            self._redraw_bars()

    def _redraw_bars(self):
        width = max(self.canvas.winfo_width(), 100)
        height = max(self.canvas.winfo_height(), WAVE_CANVAS_HEIGHT)
        spacing = self.bar_width + self.bar_gap
        count = max(int(width / spacing), 3)
        self.canvas.delete('bar')
        self.bars = []
        for index in range(count):
            x0 = index * spacing
            x1 = x0 + self.bar_width
            rect = self.canvas.create_rectangle(
                x0, height, x1, height, fill=ACCENT, outline='', tags='bar'
            )
            self.bars.append(rect)
        self.canvas.config(height=height)

    def _animate(self):
        if not self.running or not self.bars:
            return
        height = max(self.canvas.winfo_height(), WAVE_CANVAS_HEIGHT)
        for rect in self.bars:
            variation = random.randint(self.BAR_MIN_HEIGHT, self.BAR_MAX_HEIGHT)
            x0, _, x1, _ = self.canvas.coords(rect)
            self.canvas.coords(rect, x0, height - variation, x1, height)
        self.animation_id = self.canvas.after(self.ANIMATION_INTERVAL, self._animate)


def _record_voice():
    if sr is None:
        _notify_voice_issue(VOICE_UNAVAILABLE_MESSAGE)
        return
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(
                source,
                timeout=VOICE_TIMEOUT,
                phrase_time_limit=VOICE_PHRASE_LIMIT,
            )
    except sr.WaitTimeoutError:
        _notify_voice_issue(VOICE_ERROR_TEMPLATE.format('No speech detected; try again sooner.'))
    except sr.UnknownValueError:
        _notify_voice_issue(VOICE_ERROR_TEMPLATE.format('I could not understand the audio.'))
    except sr.RequestError as exc:
        _notify_voice_issue(VOICE_ERROR_TEMPLATE.format(f'Recognition service error: {exc}'))
    except Exception as exc:
        _notify_voice_issue(VOICE_ERROR_TEMPLATE.format(str(exc)))
    else:
        try:
            transcript = recognizer.recognize_google(audio).strip()
        except sr.UnknownValueError:
            _notify_voice_issue(VOICE_ERROR_TEMPLATE.format('I could not understand the speech.'))
        except sr.RequestError as exc:
            _notify_voice_issue(VOICE_ERROR_TEMPLATE.format(f'Recognition service error: {exc}'))
        except Exception as exc:
            _notify_voice_issue(VOICE_ERROR_TEMPLATE.format(str(exc)))
        else:
            if transcript:
                root.after(0, lambda: send_message(transcript))
            else:
                _notify_voice_issue(VOICE_ERROR_TEMPLATE.format('Speech captured no text.'))
    finally:
        root.after(0, _reset_voice_button)


def start_voice_capture():
    if sr is None:
        append_chat('bot', VOICE_UNAVAILABLE_MESSAGE)
        return
    if wave_visualizer:
        wave_visualizer.show()
    _set_voice_button_state(text=VOICE_LISTENING_LABEL, state='disabled')
    threading.Thread(target=_record_voice, daemon=True).start()


def load_chat_history():
    entries = default_controller.load_history(limit=HISTORY_LIMIT)
    for entry in entries:
        role = entry.get('role')
        message = entry.get('message', '')
        if role == 'user':
            append_chat('user', message, animate=False)
        elif role == 'bot':
            append_chat('bot', message, animate=False)


def send_message(override: Optional[str] = None):
    raw = override if override is not None else chat_input.get()
    message = (raw or '').strip()
    if not message:
        return
    if override is None:
        chat_input.delete(0, tk.END)

    append_chat('user', message, animate=False)

    bot_message = default_controller.send_user_message(message)
    append_chat('bot', bot_message, animate=True)


chat_input = tk.Entry(root, bg=INPUT_BG, fg=INPUT_FG, relief=tk.FLAT)
chat_input.grid(row=1, column=0, sticky='ew', padx=(14, 6), pady=(0, 14), ipady=8)

send_button = tk.Button(
    root,
    text='Send',
    width=10,
    bg=ACCENT,
    fg='#ffffff',
    relief=tk.FLAT,
    command=send_message,
)
send_button.grid(row=1, column=1, sticky='e', padx=(6, 6), pady=(0, 14), ipady=4)

voice_button = tk.Button(
    root,
    text=VOICE_ICON,
    width=4,
    bg=ACCENT,
    fg='#ffffff',
    relief=tk.FLAT,
    command=start_voice_capture,
)
voice_button.grid(row=1, column=2, sticky='e', padx=(6, 14), pady=(0, 14), ipady=4)

wave_frame = tk.Frame(root, bg=ROOT_BG)
wave_frame.grid(row=2, column=0, columnspan=3, sticky='ew', padx=14, pady=(0, 14))
wave_canvas = tk.Canvas(wave_frame, height=WAVE_CANVAS_HEIGHT, bg=ROOT_BG, highlightthickness=0)
wave_canvas.pack(fill='x', pady=(4, 0))
wave_visualizer = WaveVisualizer(wave_frame, wave_canvas)
wave_frame.grid_remove()

root.bind('<Return>', lambda event: send_message())

load_chat_history()
root.mainloop()
