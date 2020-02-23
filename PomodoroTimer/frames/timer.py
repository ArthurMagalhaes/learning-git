import tkinter as tk
from tkinter import ttk
from collections import deque


class Timer(ttk.Frame):
    def __init__(self, parent, controller, show_settings):
        super().__init__(parent)

        self.controller = controller
        pomodoro_time = int(controller.pomodoro.get())
        self.current_time = tk.StringVar(value=f'{pomodoro_time:2d}:00')

        self.current_time_label = tk.StringVar(value=controller.timer_schedule[0])
        self.timer_running = False
        self._timer_decrement_job = None

        timer_description = ttk.Label(self, textvariable=self.current_time_label)
        timer_description.grid(row=0, column=0, sticky='W', padx=(10, 0), pady=(10, 0))
        settings_button = ttk.Button(
            self,
            text='Settings',
            command=show_settings,
            cursor='hand2'
        )
        settings_button.grid(row=0, column=1, sticky='E', padx=10, pady=(10, 0))

        timer_frame = ttk.Frame(self, height='100')
        timer_frame.grid(pady=(10, 0), sticky='NESW')

        timer_counter = ttk.Label(timer_frame, textvariable=self.current_time)
        timer_counter.grid()
        timer_counter.place(relx=0.5, rely=0.5, anchor='center')

        button_container = ttk.Frame(padding=10)
        button_container.grid(row=2, sticky='EW')
        button_container.columnconfigure((0, 1), weight=1)

        self.start_button = ttk.Button(button_container, text='Start', command=self.start_timer, cursor='hand2')
        self.start_button.grid(row=0, column=0, sticky='EW')
        self.stop_button = ttk.Button(button_container, text='Stop', state='disable',
                                      command=self.stop_timer, cursor='hand2')
        self.stop_button.grid(row=0, column=1, sticky='EW')
        self.reset_button = ttk.Button(button_container, text='Reset', command=self.reset_timer, cursor='hand2')
        self.reset_button.grid(row=0, column=2, sticky='EW')

        self.decrement_time()

    def start_timer(self):
        self.timer_running = True
        self.start_button['state'] = 'disable'
        self.stop_button['state'] = 'enable'
        self.decrement_time()

    def stop_timer(self):
        self.timer_running = False
        self.start_button['state'] = 'enable'
        self.stop_button['state'] = 'disable'

        if self._timer_decrement_job:
            self.after_cancel(self._timer_decrement_job)
            self._timer_decrement_job = None

    def reset_timer(self):
        self.start_timer()
        pomodoro_time = int(self.controller.pomodoro.get())
        self.current_time = tk.StringVar(value=f'{pomodoro_time:02d}:00')
        self.controller.timer_schedule = deque(self.controller.timer_order)
        self.current_time_label.set(self.controller.timer_schedule[0])

    def decrement_time(self):
        current_time = self.current_time.get()

        if self.timer_running and current_time != '00:00':
            minutes, seconds = current_time.split(':')
            minutes = int(minutes)
            seconds = int(seconds)

            if seconds > 0:
                seconds -= 1
            else:
                seconds, minutes = 59, minutes - 1

            self.current_time.set(f'{minutes:02d}:{seconds:02d}')
            self._timer_decrement_job = self.after(1000, self.decrement_time())
            self.after(1000, self.decrement_time)

        elif self.timer_running and current_time == '00:00':
            self.controller.timer_schedule.rotate(-1)
            next_up = self.controller.timer_schedule[0]
            self.current_time_label.set(next_up)

            if next_up == 'Pomodoro':
                self.current_time.set('25:00')
            elif next_up == 'Short Break':
                self.current_time.set('05:00')
            elif next_up == 'Long Break':
                self.current_time.set('15:00')

            self.after(1000, self.decrement_time)
