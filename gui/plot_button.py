import tkinter as tk

from threading import Thread


class PlotButton(tk.Button):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Button.__init__(self, self.parent, text="Plot")

    def build_button(self, graph, set_plot):
        self.is_plotting = False
        self.config(command=lambda: self.on_button_press(graph, set_plot))

    def on_button_press(self, graph, set_plot):
        if self.is_plotting:
            return

        self.is_plotting = True

        def thread_set_plot():
            set_plot(graph)
            self.is_plotting = False

        command = Thread(target=thread_set_plot)
        command.start()
