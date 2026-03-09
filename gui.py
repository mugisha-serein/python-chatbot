import tkinter as tk
from tkinter import scrolledtext
from engine import get_response


root = tk.Tk()
root.title("Python Chatbot")
root.geometry("400x600")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled')
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

chat_input = tk.Entry(root, width=40)
chat_input.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X, expand=True)

def send_message():
    message = chat_input.get().strip()
    if message:
        chat_area.config(state='normal')
        chat_area.insert(tk.END, "You: " + message + "\n")
        
        bot_message = get_response(message)
        chat_area.insert(tk.END, "Bot: " + bot_message + "\n")
        
        chat_area.config(state='disabled')
        chat_input.delete(0, tk.END)

send_button = tk.Button(root, text="Send", width=10, command=send_message)
send_button.pack(padx=10, pady=10)

root.bind('<Return>', lambda event: send_message())

root.mainloop()