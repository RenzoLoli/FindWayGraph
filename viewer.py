import graphviz as gv

from nodes import Node
from edges import Edge

from typing import Tuple


class GraphViewerStrattegy:
    def __init__(self) -> None:
        pass

    def add_node(self, _: Node) -> None:
        pass

    def add_edge(self, _: Edge) -> None:
        pass

    def export(self, directory: str, filename: str, view: bool) -> None:
        pass

    def clear(self):
        pass

    def pipe(self) -> bytes:
        return bytes()

    def get_scaled_coords(self, _: Tuple[float, float]):
        pass


class GraphVizViewerStrattegy(GraphViewerStrattegy):
    def __init__(self) -> None:
        self.graph_scale = 350
        self.graph = gv.Digraph(comment="Location Table", format="jpeg", engine="neato")

    def clear(self):
        self.graph.clear()

    def add_node(self, node: Node) -> None:
        coords = (node.x, node.y)
        scale_coords = self.get_scaled_coords(coords)
        self.graph.node(
            node.osmid,
            f'{coords}', 

            pos=f'{scale_coords[0]}, {scale_coords[1]}!',
            shape="point",
        )

    def get_scaled_coords(self, coords: Tuple[float, float]):
        return (coords[0] * self.graph_scale, coords[1] * self.graph_scale)

    def add_edge(self, edge: Edge) -> None:
        self.graph.edge(edge.u, edge.v, style="solid", arrowsize="0", **edge.attrs)

    def export(self, directory: str, filename: str, view: bool):
        self.graph.render(filename=filename, directory=directory, view=view)

    def pipe(self) -> bytes:
        # retorna la imagen del grapho en bytes
        return self.graph.pipe()
