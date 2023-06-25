import random
import tkinter as tk
from typing import Callable, List, Tuple
from tkintermapview import TkinterMapView
from tkintermapview.canvas_path import CanvasPath

from edges import Edge
from logger import Logger

def random_color() -> str:
    r = lambda: random.randint(0,255)
    return ('#%02X%02X%02X' % (r(),r(),r()))

class MapViewer(TkinterMapView):
    def __init__(self, parent: tk.Frame):
        self.parent = parent
        self.servers = ["m", "s"]
        self.server = -1
        TkinterMapView.__init__(self, self.parent, corner_radius=0)

        self.change_server()
        self.set_zoom(14)
        self.set_position(-12.0599213, -77.0350861)
        self.add_right_click_menu_command(
            label="Change Viewer",
            command=self.change_server,
            pass_coords=False
        )
        # self.set_overlay_tile_server("http://a.tiles.openrailwaymap.org/standard/{z}/{x}/{y}.png")  # railway infrastructure

        self.last_source_marker = None
        self.last_destination_marker = None

    def change_server(self):
        self.server = (self.server + 1) % len(self.servers)
        self.set_tile_server("https://mt0.google.com/vt/lyrs="+self.servers[self.server]+"&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

    def set_route(self, src: Tuple[float, float], dst: Tuple[float, float], paths: List[List[Tuple[float, float]]]):
        self.clear_markers()
        self.last_source_marker = self.set_marker(src[1], src[0])
        self.last_destination_marker = self.set_marker(dst[1], dst[0])
        self.set_new_path(paths)

    def set_source(self, coord: Tuple[float, float]):
        if self.last_source_marker:
            self.last_source_marker.delete()

        self.set_position(coord[1], coord[0])
        self.set_zoom(18)
        self.last_source_marker = self.set_marker(coord[1], coord[0])

    def clear_markers(self):
        if self.last_source_marker:
            self.last_source_marker.delete()
        if self.last_destination_marker:
            self.last_destination_marker.delete()

    def clear_path(self):
        self.delete_all_path()

    def set_destination(self, coord: Tuple[float, float]):
        if self.last_destination_marker:
            self.last_destination_marker.delete()

        self.set_position(coord[1], coord[0])
        self.set_zoom(18)
        self.last_destination_marker = self.set_marker(coord[1], coord[0])

    def set_new_path(self, connections: List[List[Tuple[float, float]]]):
        self.clear_path()
        color = random_color()
        for connection in connections:
            path = [coord[::-1] for coord in connection]
            self.set_path(path, width=3, color=color)