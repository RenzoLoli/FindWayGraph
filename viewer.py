import graphviz as gv

from nodes import Node
from edges import Edge


class GraphViewerStrattegy:
    def __init__(self) -> None:
        self.graph = gv.Digraph(format="png", engine="neato")
        pass

    def add_node(self, node: Node) -> None:
        pass

    def add_edge(self, edge: Edge) -> None:
        pass

    def export(self, directory: str, filename: str) -> None:
        pass

    def pipe(self):
        pass


class GraphVizViewerStrattegy(GraphViewerStrattegy):
    def __init__(self) -> None:
        self.graph_scale = 1000
        self.graph = gv.Digraph(comment="Location Table", format="jpeg", engine="neato")

    def add_node(self, node: Node) -> None:
        self.graph.node(
            node.osmid,
            str(str(node.x) + "-" + str(node.y)),
            pos=str(
                str(node.x * self.graph_scale)
                + ","
                + str(node.y * self.graph_scale)
                + "!"
            ),
            shape="point",
        )

    def add_edge(self, edge: Edge) -> None:
        self.graph.edge(edge.u, edge.v, style="solid", arrowsize="1")

    def export(self, directory: str, filename: str):
        self.graph.render(filename=filename, directory=directory, view=False)

    def pipe(self):
        # retorna la imagen del grapho generado
        return self.graph.pipe()
