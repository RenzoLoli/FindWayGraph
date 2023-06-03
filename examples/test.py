from ..graph import Graph
from ..viewer import GraphVizViewerStrattegy
from ..logger import Logger
from ..loader import Loader

from os import path

# grafo principal
graph = Graph(GraphVizViewerStrattegy())

# cargar datos
Logger.status('Importando datos a memoria')

loader = Loader()
loader.load_nodes(path.abspath("resources/nodes.xlsx"), "A:G", 3325, graph.add_node)
loader.load_edges(path.abspath("resources/edges.xlsx"), "A:Q", 7665, graph.add_edge)

Logger.success('Archivos importados satisfactoriamente')

# exportar a png
Logger.status('Exportando grafo')

EXPORT_DIR = path.abspath('output')
EXPORT_FILENAME = 'map'
graph.export(directory=EXPORT_DIR, filename=EXPORT_FILENAME)

Logger.success('Archivo exportado satisfactoriamente')
