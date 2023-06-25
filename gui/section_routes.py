import tkinter as tk
from typing import Tuple

from gui.routes import Route

class SectionRoutes(tk.Text):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Text.__init__(self, self.parent)
        self.rows = 0
        self.last_selected_row = "0.0"
        self.bind('<ButtonRelease-1>', lambda _: self.select_row())
        self.tag_configure("selected", background="blue", foreground= "white")

    def select_row(self):
        row = self.index(tk.CURRENT + " linestart")
        self.tag_remove("selected", self.last_selected_row, self.index(self.last_selected_row + " lineend"))
        self.tag_add("selected", row, self.index(row + " lineend"))        
        self.last_selected_row = row

    def new_route(self, src: Tuple[float, float], dst: Tuple[float, float], alg: str) -> None:
        line = ""
        if self.rows != 0: line += "\n"
        line += f"{src} -> {dst} {alg}"
        self.insert(tk.END, line)
        self.see(tk.END)
        self.rows += 1

    def clear_all(self) -> None:
        self.delete(1.0, tk.END)
        self.tag_remove("selected", "0.0", tk.END)
        self.rows = 0

    def update_routes(self, routes: list[Tuple[Tuple[float, float], Tuple[float, float], str]], has_new: bool = False) -> None:
        self.clear_all()
        for route in routes:
            self.new_route(*route)

        if has_new:
            self.last_selected_row = self.index(tk.CURRENT + " linestart")
        
        selected = self.get_selected()
        self.tag_add("selected", selected, self.index(selected + " lineend"))   

    def get_selected_row(self) -> int:
        return int(self.get_selected().split('.')[0]) - 1
    
    def get_selected(self) -> str:
        return self.last_selected_row

    def get_rows(self) -> int:
        return self.rows