import tkinter as tk

from .input_src import InputSrc
from .input_dst import InputDst
from .log_area import LogArea
from .plot_canvas import PlotCanvas
from .plot_button import PlotButton

class Window:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self._init_components()

    def _init_components(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 1150
        window_height = 550
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.title("Map")
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

        section_main = tk.Frame(self.window, bg="black")
        section_main.columnconfigure(0, weight=1)
        section_main.columnconfigure(1, weight=1)
        section_main.rowconfigure(0, weight=1)
        section_main.grid(row=0, column=0, sticky="nsew")

        section_1 = tk.Frame(section_main, bg="red")
        section_1.columnconfigure(0, weight=1)
        section_1.rowconfigure(0, weight=1)
        section_1.rowconfigure(1, weight=1)
        section_1.rowconfigure(2, weight=1)
        section_1.rowconfigure(3, weight=2)
        section_1.grid_propagate(False)
        section_1.grid(row=0, column=0, sticky="nsew")

        self.plot_button = PlotButton(section_1)
        self.plot_button.grid(row=0, column=0, sticky="nsew")

        self.input_src = InputSrc(section_1)
        self.input_src.grid(row=1, column=0, sticky="nsew")

        self.input_dst = InputDst(section_1)
        self.input_dst.grid(row=2, column=0, sticky="nsew")

        self.log_area = LogArea(section_1)
        self.log_area.grid(row=3, column=0, sticky="nsew")

        section_2 = tk.Frame(section_main, bg="blue")
        section_2.columnconfigure(0, weight=1)
        section_2.rowconfigure(0, weight=1)
        section_2.grid_propagate(False)
        section_2.grid(row=0, column=1, sticky="nsew")

        self.buffer_canvas = PlotCanvas(section_2)
        self.buffer_canvas.grid(row=0, column=0, sticky="nsew")

    def build_plot_button(self, graph):
        self.plot_button.build_button(graph, self.buffer_canvas.set_plot)

    def get_logger(self):
        return self.log_area.log

    def run(self):
        self.window.mainloop()
