
import tkinter as tk
import io

from threading import Thread
from typing import Any
from PIL import Image, ImageTk


def clamp(value, _min, _max):
    return min(_max, max(_min, value))


class Window:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self._init_components()

    def _init_components(self):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 1000
        window_height = 500
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        section_1 = tk.Frame(self.window, width=500, height=500)
        section_1.pack(side=tk.LEFT, padx=5)

        input_label = tk.Label(section_1, text="Input:")
        input_label.pack()

        self.input_entry = tk.Entry(section_1, width=30)
        self.input_entry.pack()

        self.input_button = tk.Button(section_1, text="Register")
        self.input_button.pack()

        self.log_text = tk.Text(section_1, width=50, height=20)
        self.log_text.pack()

        section_2 = tk.Frame(self.window, width=700, height=500)
        section_2.pack(side=tk.LEFT, padx=5)

        self.image = Image.new(Image.MODES[0], (0, 0))
        self.photo = ImageTk.PhotoImage(self.image)
        self.zoom_factor = 1.0
        self.zoom_rate = 1.15
        self.canvas = tk.Canvas(section_2, width=600, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas_id = self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.canvas.bind("<B1-Motion>", self.on_mousepressmotion)
        self.canvas.bind("<Button-1>", self.on_mousepress)

    def on_mousewheel(self, event):
        self.zoom_in() if event.delta > 0 else self.zoom_out()

    def on_mousepress(self, event):
        self.mouse_pos = (event.x, event.y)

    def on_mousepressmotion(self, event: tk.Event):
        new_mouse_pos = (event.x, event.y)
        offset = (
            new_mouse_pos[0] - self.mouse_pos[0],
            new_mouse_pos[1] - self.mouse_pos[1],
        )

        self.mouse_pos = new_mouse_pos

        self.canvas.move(self.canvas_id, offset[0], offset[1])

    def component_size(self, component):
        return (component.winfo_width(), component.winfo_height())

    def build_button(self, graph):
        self.is_plotting = False
        self.input_button.config(command=lambda: self.on_button_press(graph))

    def on_button_press(self, graph):
        if self.is_plotting:
            return

        self.is_plotting = True

        def thread_set_plot():
            self.set_plot(graph)
            self.is_plotting = False

        command = Thread(target=thread_set_plot)
        command.start()

    def run(self):
        self.window.mainloop()

    def zoom_in(self):
        self.zoom_factor = clamp(self.zoom_factor * self.zoom_rate, 0.1, 6.0)
        self.zoom_image()

    def zoom_out(self):
        self.zoom_factor = clamp(self.zoom_factor / self.zoom_rate, 0.1, 6.0)
        self.zoom_image()

    def zoom_image(self):
        img_size = self.image.size

        new_size = (
            int(img_size[0] * self.zoom_factor),
            int(img_size[1] * self.zoom_factor),
        )

        self.buffer = self.image.resize(new_size, Image.NEAREST)
        self.update_canvas()

    def update_canvas(self):
        self.photo = ImageTk.PhotoImage(self.buffer)
        self.canvas.itemconfigure(self.canvas_id, image=self.photo)

    def set_plot(self, graph):
        plot = graph.pipe()
        self.image = Image.open(io.BytesIO(plot))
        self.buffer = self.image.copy()
        self.update_canvas()

    def log(self, msg: Any):
        self.log_text.insert(tk.END, str(msg) + "\n")
        self.log_text.see(tk.END)
