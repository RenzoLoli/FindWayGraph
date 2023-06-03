import tkinter as tk


class InputSrc(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weigh=1)
        self.rowconfigure(0, weigh=1)
        self._init_components()

    def _init_components(self):
        self.input_label = tk.Label(self, text="Origen:")
        self.input_label.grid(row=0, column=0, sticky="nsew")

        self.input_entry = tk.Entry(self)
        self.input_entry.grid(row=0, column=1, sticky="nsew")
