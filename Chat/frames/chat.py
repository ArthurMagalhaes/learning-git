import tkinter as tk
from tkinter import ttk
import requests
from datetime import datetime
from PIL import Image, ImageTk

messages = [{"message": "Hello, world", "date": 15498487}]
message_labels = []


class Chat(ttk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.messages_frame = ttk.Frame(self)
        self.messages_frame.grid(row=0, column=0, sticky='NSEW', pady=5)

        input_frame = ttk.Frame(self, padding=10)
        input_frame.grid(row=1, column=0, sticky="EW")

        message_fetch = ttk.Button(
            input_frame,
            text="Fetch",
            command=self.get_messages
        )
        message_fetch.pack()

    def get_messages(self):
        global messages
        messages = requests.get("http://167.99.63.70/messages").json()
        # print(messages)
        self.update_message_widgets()

    def update_message_widgets(self):
        existing_labels = [(message['text'], time['text']) for message, time in message_labels]

        for message in messages:
            message_time = datetime.fromtimestamp(message['date']).strftime(' %d-%m-%Y %H:%M:%S')
            if message['message'] not in existing_labels:
                container = ttk.Frame(self.messages_frame)
                container.columnconfigure(1, weiht=1)
                container.grid(sticky='EW', padx=(0, 50), pady=10)

                time_label = ttk.Label(container, text=message_time)
                message_label = ttk.Label(self.messages_frame, text=message['message'], anchor='w', justify='left')
                message_label.grid(sticky='NSEW')

                message_labels.append((message_label, time_label))

    def _create_message_container(self, message_content, message_time, message_labels):
        container = ttk.Frame(self.messages_frame)
        container.columnconfigure(1, weiht=1)
        container.grid(sticky='EW', padx=(0, 50), pady=10)

        self._create_message_bubble(container, message_content, message_time, message_labels)

    def _create_message_bubble(self, container, message_content, message_time, message_labels):
        time_label = ttk.Label(container, text=message_time)
        time_label.grid(sticky='NSEW')
