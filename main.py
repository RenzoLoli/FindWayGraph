from graph import Graph
from loader import Loader
from viewer import GraphVizViewerStrattegy
from os import path

from logger import Logger
from gui.gui import Window

def create_graph():
    # grafo principal
    graph = Graph(GraphVizViewerStrattegy())

    # cargar datos
    loader = Loader()
    loader.load_nodes(path.abspath("resources/nodes.xlsx"), "A:G", 3325, graph.add_node)
    loader.load_edges(path.abspath("resources/edges.xlsx"), "A:Q", 7665, graph.add_edge)

    return graph

def main():
    window = Window()
    Logger.set_logger(window.get_logger())

    graph = create_graph()
    window.build_plot_button(graph)

    window.run()
if __name__ == "__main__":
    main()
