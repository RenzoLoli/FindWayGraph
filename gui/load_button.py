from threading import Thread
import tkinter as tk
from typing import Any

class LoadButton(tk.Button):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Button.__init__(self, self.parent, text="Load", background="#777777", foreground="#000000")

    def set_cmd(self, cmd):
        def pseudo_cmd():
            cmd()
            self.config(state="active")

        self.load_thread = Thread(target=pseudo_cmd)

        def handle_cmd():
            self.config(state="disabled")
            self.load_thread.start()
            self.load_thread = Thread(target=pseudo_cmd)

        self.config(command=handle_cmd)