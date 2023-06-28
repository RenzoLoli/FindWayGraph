import time
import tkinter as tk
from tkinter import filedialog
from typing import List, Tuple
from os import path
from gui.routes import Route, Routes
from gui.section_1 import Section1
from gui.section_2 import Section2
from loader import Loader

from logger import Logger
from viewer import GraphVizViewerStrattegy
from graph import Graph


class Window:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.graph = Graph(GraphVizViewerStrattegy())
        self.routes = Routes()
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
        section_main.columnconfigure(1, weight=3)
        section_main.rowconfigure(0, weight=1)
        section_main.grid(row=0, column=0, sticky="nsew")

        self.buffer_route = Route("", "", Graph.get_algorithms()[0])

        # Section 1
        self.s1 = Section1(section_main)
        self.s1.load_button.set_cmd(self.load_graph)

        self.s1.section_config.alg_entry.sibling.bind("<<ComboboxSelected>>", self.combobox_changed)
        self.s1.section_config.new_button.config(command=self.new_route)
        self.s1.section_config.save_button.config(command=self.save_route)
        self.s1.section_config.clear_all_button.config(command=self.delete_all_routes)
        self.s1.section_config.duplicate_button.config(command=self.duplicate_route)
        def section_routes_ButtonRelease_1(_):  
            self.s1.section_routes.select_row()
            selected = self.s1.section_routes.get_selected_row()
            if self.routes.empty():
                Logger.error("No routes loaded")
                return
            
            list_routes = self.routes.as_list()
            route = list_routes[selected]

            self.buffer_route.copy(route=route)

            src = self.graph.get_node(route.src_osmid)
            dst = self.graph.get_node(route.dst_osmid)

            self.s1.section_config.update_form(src.to_coords()[::-1], dst.to_coords()[::-1], route.algorithm)
            self.s2.map_viewer.set_route(src.to_coords(), dst.to_coords(), route.path)

        self.s1.section_routes.bind('<ButtonRelease-1>', section_routes_ButtonRelease_1)
        self.s1.section_config.alg_entry.sibling.config(values=Graph.get_algorithms())
        self.s1.section_config.alg_entry.sibling.current(0)

        self.s1.test_algorithm_button.config(command=self.test_algorithm)

        self.s1.grid(row=0, column=0, sticky="nsew")

        # Section 2
        self.s2 = Section2(section_main)
        self.s2.map_viewer.add_right_click_menu_command(label="Add Source", 
                                                        command=self.set_source,
                                                        pass_coords=True)
        self.s2.map_viewer.add_right_click_menu_command(label="Add Destination", 
                                                        command=self.set_destination, 
                                                        pass_coords=True)
        self.s2.grid(row=0, column=1, sticky="nsew")

    def set_source(self, coords: Tuple[str, str]) -> None:
        norm_coords = (float(coords[1]), float(coords[0]))
        nearest = self.graph.calc_nearest_node(norm_coords)
        if nearest is None:
            Logger.error("did not find node for source")
            return None
        self.buffer_route.src_osmid = nearest.osmid

        nearest_coord = nearest.to_coords()

        self.s1.section_config.set_source(nearest_coord[::-1])
        self.s2.map_viewer.set_source(nearest_coord)
        self.s2.map_viewer.clear_path()

    def set_destination(self, coords: Tuple[str, str]) -> None:
        norm_coords = (float(coords[1]), float(coords[0]))
        nearest = self.graph.calc_nearest_node(norm_coords)
        if nearest is None:
            Logger.error("did not find node for destination")
            return None
        
        self.buffer_route.dst_osmid = nearest.osmid

        nearest_coord = nearest.to_coords()
        
        self.s1.section_config.set_destination(nearest_coord[::-1])
        self.s2.map_viewer.set_destination(nearest_coord)
        self.s2.map_viewer.clear_path()

    def combobox_changed(self, _):
        self.buffer_route.algorithm = self.s1.section_config.alg_entry.sibling.get()
        self.s2.map_viewer.clear_path()

    def parse_route(self, route: Route) -> Tuple[Tuple[float, float], Tuple[float, float], str]:
        src_coord = self.graph.get_node(route.src_osmid).to_coords()
        dst_coord = self.graph.get_node(route.dst_osmid).to_coords()
        algorithm = route.algorithm
        return (src_coord, dst_coord, algorithm)
    
    def normalize_routes(self) -> List[Tuple[Tuple[float, float], Tuple [float, float], str]]:
        return list(map(self.parse_route, self.routes.as_list()))

    def new_route(self) -> None:
        
        if not self.buffer_route.is_valid():
            Logger.error("Empty route")
            return None
        
        n_route = self.routes.new(self.buffer_route)
        n_route.path = self.search_path(n_route.src_osmid, n_route.dst_osmid, n_route.algorithm)

        self.s2.map_viewer.set_new_path(n_route.path)
        
        src = self.graph.get_node(n_route.src_osmid)
        dst = self.graph.get_node(n_route.dst_osmid)

        self.s2.map_viewer.set_source(src.to_coords())
        self.s2.map_viewer.set_destination(dst.to_coords())

        norm_routes = self.normalize_routes()
        self.s1.section_routes.update_routes(norm_routes, True)

    def save_route(self) -> None:
        if not self.buffer_route.is_valid():
            Logger.error("Empty route")
            return None

        if self.routes.empty():
            Logger.error("No available routes")
            return None

        selected_row = self.s1.section_routes.get_selected_row()
        route = self.routes.get(selected_row)

        route.copy(route=self.buffer_route)

        route.path = self.search_path(route.src_osmid, route.dst_osmid, route.algorithm)
        self.s2.map_viewer.set_new_path(route.path)

        norm_routes = self.normalize_routes()
        self.s1.section_routes.update_routes(norm_routes)

    def duplicate_route(self):
        if self.routes.empty():
            Logger.error("No available routes")
            return None
        
        selected_row = self.s1.section_routes.get_selected_row()
        route = self.routes.get(selected_row)

        self.buffer_route.copy(route=route)
        self.buffer_route.path = route.path.copy()

        self.new_route()

    def delete_all_routes(self) -> None:
        self.routes.clear()
        self.s2.map_viewer.clear_markers()
        self.s2.map_viewer.clear_path()

        norm_routes = self.normalize_routes()
        self.s1.section_routes.update_routes(norm_routes)

    def search_path(self, src_osmid: str, dst_osmid: str, algorithm: str) -> List:
        searched_path = []

        if algorithm not in Graph.get_algorithms():
            Logger.error("Invalid algorithm")
            return searched_path

        finder = self.graph.choose_algorithm(algorithm)

        start = time.time()
        searched_path = finder(src_osmid, dst_osmid)
        end = time.time()

        Logger.info(f"Algorithm: {algorithm}")
        Logger.info(f"Took {end - start} seconds")
        Logger.info(f"Path length: {len(searched_path)}")
        
        edges = self.graph.osmids_to_edges(searched_path)
        path = list(map(lambda edge: edge.to_path(), edges))
        return path
    
    def test_algorithm(self) -> None:       
        if self.routes.empty():
            Logger.error("No available routes")
            return None
        
        selected_row = self.s1.section_routes.get_selected_row()
        route = self.routes.get(selected_row)

        finder = self.graph.choose_algorithm(route.algorithm)

        max_iterations = 10
        accum = 0
        for i in range(max_iterations):
            start = time.time()
            finder(route.src_osmid, route.dst_osmid)
            end = time.time()
            accum += end - start
        
        Logger.info(f"'{route.algorithm}' -> {accum / max_iterations:4f}'s on {max_iterations} iterations")


    def ask_filenames(self) -> Tuple[str]:
        filepaths = filedialog.askopenfilenames(initialdir=path.abspath("."))
        return filepaths # type: ignore

    def load_graph(self) -> None:
        paths = self.ask_filenames()

        paths = [""]
        if len(paths) == 0: 
            Logger.error("nombre de archivo erroneo")
            return None

        self.graph.clear()
        
        Logger.info(f"Cargando '{paths}'")

        loader = Loader()
        for path in iter(paths):
            loader.load_nodes( #3325
                path, "A:G", None, self.graph.add_node
            )

        for path in iter(paths):
            loader.load_edges( #7665
                path, "A:Q", None, self.graph.add_edge
            )

        self.graph.sort_nodes()
        nodes = self.graph.get_nodes()
        half = int(len(nodes) / 2)
        half_node = nodes[half].to_coords()
        self.s2.map_viewer.set_position(half_node[1], half_node[0])

        Logger.info("Grafo cargado!")

    def get_logger(self):
        return self.s2.log_area.log

    def run(self):
        self.window.mainloop()
