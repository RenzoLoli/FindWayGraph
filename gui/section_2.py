import tkinter as tk
from typing import Any
from gui.log_area import LogArea

from gui.map_view import MapViewer

class Section2(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)
        self.columnconfigure(0, weight=3)
        self.rowconfigure(0, weight=3, uniform='none')
        self.rowconfigure(1, weight=1, uniform='none')
        self.grid_propagate(False)

        self._init_widget()

    def _init_widget(self) -> None:
        self.map_viewer = MapViewer(self)
        self.map_viewer.grid(row=0, column=0, sticky="nsew")

        self.log_area = LogArea(self)
        self.log_area.grid(row=1, column=0, sticky="nsew")

    def clear_routes(self):
        self.map_viewer.delete_all_path()
        self.map_viewer.delete_all_marker()
