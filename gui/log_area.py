import tkinter as tk
from typing import Any

class LogArea(tk.Text):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Text.__init__(self, self.parent)

    def log(self, msg: Any):
        self.insert(tk.END, str(msg) + "\n")
        self.see(tk.END)
