import tkinter as tk

class LabelFrame(tk.Frame):
    def __init__(self, parent, text, sibling):
        self.parent = parent
        tk.Frame.__init__(self, self.parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.rowconfigure(0, weight=1)

        self.label = tk.Label(self, text=text)
        self.label.grid(row=0, column=0, sticky="nsew")
        
        self.sibling = sibling(self)
        self.sibling.grid(row=0, column=1, sticky="nsew")
    
    def get_sibling(self):
        return self.sibling