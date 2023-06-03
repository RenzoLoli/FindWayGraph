import tkinter as tk
import io
from PIL import Image, ImageTk

def clamp(value, _min, _max):
    return min(_max, max(_min, value))

class PlotCanvas(tk.Canvas):
    def __init__(self, parent: tk.Frame) -> None:
        self.parent = parent
        tk.Canvas.__init__(self, self.parent)
        self._init_components()

    def _init_components(self):
        self.image = Image.new(Image.MODES[0], (0, 0))
        self.photo = ImageTk.PhotoImage(self.image)
        self.zoom_factor = 1.0
        self.zoom_rate = 1.15
        self.canvas_id = self.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.bind("<MouseWheel>", self.on_mousewheel)
        self.bind("<B1-Motion>", self.on_mousepressmotion)
        self.bind("<Button-1>", self.on_mousepress)

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

        self.move(self.canvas_id, offset[0], offset[1])

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
        self.itemconfigure(self.canvas_id, image=self.photo)

    def set_plot(self, graph):
        plot = graph.pipe()
        self.image = Image.open(io.BytesIO(plot))
        self.buffer = self.image.copy()
        self.update_canvas()
