from nodes import Nodes, Node
from edges import Edges, Edge

from viewer import GraphViewerStrattegy

class Graph:
    def __init__(self, viewer_strattegy: GraphViewerStrattegy) -> None:
        self.nodes = Nodes()
        self.edges = Edges()
        self.viewer = viewer_strattegy

    def add_node(self, node: Node) -> None:
        self.nodes.add_node(node)
        self.viewer.add_node(node)

    def add_edge(self, edge: Edge) -> None:
        self.validate_edge(edge)
        self.edges.add_edge(edge)
        self.viewer.add_edge(edge)

    def validate_edge(self, edge) -> bool:
        nodes_filtered = self.nodes.to_list()
        has_u = edge.u in nodes_filtered
        has_v = edge.v in nodes_filtered
        if not has_u or not has_v:
            print(f"[?] En la arista {edge.u, edge.v}")
            if not has_u:
                print(f"\t[x] No existe el nodo {edge.u}")
            if not has_v:
                print(f"\t[x] No existe el nodo {edge.v}")
            return False
        return True

    def export(self, directory, filename) -> None:
        self.viewer.export(directory,filename)

    def pipe(self):
        return self.viewer.pipe()
