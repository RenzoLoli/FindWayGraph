import osmnx as ox
import networkx as nx
import pydot
from IPython.display import Image

# Definir los lugares de origen y destino
origen = "Lima Peru"
destino = "UPC Peru San Isidro"

grafo2=ox.geocode_to_gdf(destino,which_result=1)
# print(grafo2)
# Obtener la red de carreteras de OpenStreetMap para el área de interés
grafo = ox.graph_from_address(origen, network_type="all")
print(grafo)
# print(grafo)
# coordenadas_origen = ox.geocode(origen)
# coordenadas_destino = ox.geocode(destino)
# print(coordenadas_origen[1])

# # Obtener los nodos más cercanos a las coordenadas de origen y destinoc
# coordenadas_origen = ox.nearest_nodes(grafo, x=float(coordenadas_origen[1]), y=float(coordenadas_origen[0]))
# coordenadas_destino = ox.nearest_nodes(grafo, x=coordenadas_destino[1], y=coordenadas_destino[0])
# origen_nodo = ox.nearest_nodes(grafo, coordenadas_origen[1], coordenadas_origen[0])
# destino_nodo = ox.nearest_nodes(grafo, coordenadas_destino[1], coordenadas_destino[0])
# # Calcular la ruta más corta entre los nodos de origen y destino
# ruta = nx.shortest_path(grafo, origen_nodo, destino_nodo, weight="length")

# # Crear un subgrafo que contenga únicamente los nodos y arcos de la ruta
# subgrafo = grafo.subgraph(ruta)

# # Generar el gráfico utilizando pydot
# dot = nx.nx_pydot.to_pydot(subgrafo)

# # Configurar los atributos del gráfico
# dot.set_graph_defaults(splines='true', overlap='false', sep='1', rankdir='LR')

# # Guardar el gráfico en un archivo DOT
# dot.write('ruta_graphviz.dot')

# # Generar la imagen a partir del archivo DOT utilizando Graphviz
# Image(dot.create_png())