import tkinter as tk
from typing import Any

from gui.load_button import LoadButton
from gui.log_area import LogArea
from gui.section_config import SectionConfig
from gui.section_routes import SectionRoutes

class Section1(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2, uniform="none")
        self.rowconfigure(1, weight=3, uniform="none")
        self.rowconfigure(2, weight=1, uniform="none")
        self.grid_propagate(False)

        self._init_widgets()

    def _init_widgets(self):
        self.section_config = SectionConfig(self)
        self.section_config.grid(row=0, column=0, sticky="nsew")

        self.section_routes = SectionRoutes(self)
        self.section_routes.grid(row=1, column=0, sticky="nsew")

        self.load_button = LoadButton(self)
        self.load_button.grid(row=2, column=0, sticky="nsew")