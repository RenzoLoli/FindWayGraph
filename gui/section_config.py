import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

from gui.LabelFrame import LabelFrame
from gui.routes import Route
from logger import Logger

class SectionConfig(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Frame.__init__(self, self.parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)  
        self.rowconfigure(3, weight=1)
        self.grid_propagate(False)

        self._init_components()

    def _init_components(self):
        self.src_entry = LabelFrame(self, text="Source", sibling=tk.Entry)
        self.src_entry.grid(row=0, column=0, sticky="nsew")
        
        self.dst_entry = LabelFrame(self, text="Destination", sibling=tk.Entry)
        self.dst_entry.grid(row=1, column=0, sticky="nsew")

        self.alg_entry = LabelFrame(self, text="Algorithm", sibling=ttk.Combobox)
        self.alg_entry.grid(row=2, column=0, sticky="nsew")

        section_buttons = tk.Frame(self)
        section_buttons.grid(row=3, column=0, sticky="nsew")

        section_buttons.columnconfigure(0, weight=1)
        section_buttons.columnconfigure(1, weight=1)
        section_buttons.columnconfigure(2, weight=1)
        section_buttons.columnconfigure(3, weight=1)
        section_buttons.rowconfigure(0, weight=1)

        self.new_button = tk.Button(section_buttons, text="New")
        self.new_button.grid(row=0, column=0, sticky="nsew")

        self.save_button = tk.Button(section_buttons, text="Save")
        self.save_button.grid(row=0, column=1, sticky="nsew")

        self.search_button = tk.Button(section_buttons, text="Search")
        self.search_button.grid(row=0, column=2, sticky="nsew")

        self.clear_all_button = tk.Button(section_buttons, text="Clear All")
        self.clear_all_button.grid(row=0, column=3, sticky="nsew")

    # def valiate_form(self, algorithms: List[str]) -> bool:
    #     src = self.src_entry.sibling.get()
    #     dst = self.dst_entry.sibling.get()
    #     alg = self.alg_entry.sibling.get()
        
    #     if alg not in algorithms:
    #         Logger.error("Algorithm is not valid")
    #         return False

    #     if src == "" or dst == "": 
    #         Logger.error("Source or destination is empty")
    #         return False

    #     return True
    
    def update_form(self, src: Tuple[float, float], dst: Tuple[float, float], alg: str) -> None:
        self.src_entry.sibling.delete(0, tk.END)
        self.src_entry.sibling.insert(0, src)
        self.dst_entry.sibling.delete(0, tk.END)
        self.dst_entry.sibling.insert(0, dst)
        self.alg_entry.sibling.delete(0, tk.END)
        self.alg_entry.sibling.insert(0, alg)

    def set_source(self, src: Tuple[float, float]) -> None:
        self.src_entry.sibling.delete(0, tk.END)
        self.src_entry.sibling.insert(0, src)
    
    def set_destination(self, dst: Tuple[float, float]) -> None:
        self.dst_entry.sibling.delete(0, tk.END)
        self.dst_entry.sibling.insert(0, dst)

    # def as_route(self) -> Route:
    #     src = self.src_entry.sibling.get().split(" ")
    #     dst = self.dst_entry.sibling.get().split(" ")
    #     alg = self.alg_entry.sibling.get()

    #     src = (float(src[0]), float(src[1]))
    #     dst = (float(dst[0]), float(dst[1]))

    #     return Route(src, dst, alg)
