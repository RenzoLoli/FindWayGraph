import pandas as pd
from typing import Callable
from nodes import Node
from edges import Edge
from logger import Logger


class Loader:
    def load_nodes(
        self, filename: str, cols: str, maxrows: int, every: Callable[[Node], None]
    ):
        Logger.info("Importando nodos...")

        excel = pd.read_excel(filename, usecols=cols, nrows=maxrows)
        for _, row in excel.iterrows():
            osmid = str(int(row["osmid"]))
            y = float(row["y"])
            x = float(row["x"])
            street_count = str(row["street_count"])
            highway = str(row["highway"])
            geometry = str(row["geometry"])
            n_node = Node(osmid, y, x, street_count, highway, geometry)
            every(n_node)

    def load_edges(
        self, filename: str, cols: str, maxrows: int, every: Callable[[Edge], None]
    ):
        Logger.info("Importando aristas...")

        excel = pd.read_excel(filename, usecols=cols, nrows=maxrows)
        for _, row in excel.iterrows():
            u = row["u"]
            v = row["v"]
            oneway = row["oneway"]
            name = row["name"]
            highway = row["highway"]
            reversed = row["reversed"]
            length = row["length"]
            geometry = row["geometry"]

            u = str(int(u))
            v = str(int(v))
            oneway = bool(oneway)
            name = str(name)
            highway = str(highway)
            reversed = bool(reversed)
            length = float(length)
            geometry = str(geometry)

            n_edge = Edge(u, v, oneway, name, highway, reversed, length, geometry)
            every(n_edge)
