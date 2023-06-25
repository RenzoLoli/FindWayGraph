import tkinter as tk
from typing import Any

class LogArea(tk.Text):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Text.__init__(self, self.parent, background='#000000')

        self.tag_configure('warn', foreground='yellow')
        self.tag_configure('info', foreground='green')
        self.tag_configure('error', foreground='red')

    def log(self, msg: Any, log_type: str):
        self.insert(tk.END, str(msg) + "\n", log_type)
        self.see(tk.END)
