import osmnx as ox
import pandas as pd
from shapely.geometry import LineString
from shapely.geometry import Point
# Configurar el lugar de interés
place_name = "San Miguel Lima Peru"

# Obtener el grafo de la red de carreteras con nodos
graph = ox.graph_from_place(place_name, network_type="all", simplify=False)
nodes = graph.nodes(data=True)
# Crear una lista para almacenar los datos
data_edges = []
data_nodes = []
# # Iterar sobre los segmentos de carreteras del grafo
for u, v, key, edge_data in graph.edges(keys=True, data=True):
    # Obtener las coordenadas de los nodos de inicio y fin
    u_coords = graph.nodes[u]['x'], graph.nodes[u]['y']
    v_coords = graph.nodes[v]['x'], graph.nodes[v]['y']
    if 'geometry' in edge_data:
        segment_geometry = edge_data['geometry']
    else:
        # Si no hay geometría definida, crear una línea recta entre los nodos de inicio y fin
        segment_geometry = LineString([u_coords, v_coords])
    attributes_edge = {
        'u': u,
        'v': v,
        'key': key,
        'osmid': edge_data.get('osmid', ''),
        'oneway': edge_data.get('oneway', ''),
        'lanes': edge_data.get('lanes', ''),
        'name': edge_data.get('name', ''),
        'highway': edge_data.get('highway', ''),
        'maxspeed': edge_data.get('maxspeed', ''),
        'reversed': edge_data.get('reversed', ''),
        'length': edge_data.get('length', ''),
        'geometry': segment_geometry,
        'bridge': edge_data.get('bridge', ''),
        'ref': edge_data.get('ref', ''),
        'junction': edge_data.get('junction', ''),
        'tunnel': edge_data.get('tunnel', ''),
        'access': edge_data.get('access', '')
    }
    
    # Agregar los atributos a la lista de datos
    data_edges.append(attributes_edge)

for node, attr in nodes:
    # Obtener los atributos del nodo
    y_cord = attr['y']
    x_cord = attr['x']
    geometry_node = Point(x_cord, y_cord)

    attributes_node = {
        'osmid': node,
        'y': attr['y'],
        'x': attr['x'],
        'street_count': attr.get('street_count', ''),
        'ref': attr.get('ref', ''),
        'highway': attr.get('highway', ''),
        'geometry': geometry_node
    }
    # Agregar los atributos a la lista de datos de nodos
    data_nodes.append(attributes_node)


# Crear un DataFrame de pandas con los datos
nodes_df = pd.DataFrame(data_nodes)
edges_df = pd.DataFrame(data_edges)
# Guardar el DataFrame en un archivo Excel
with pd.ExcelWriter('data_SanMiguel.xlsx') as writer:
    nodes_df.to_excel(writer, sheet_name='nodes', index=False)
    edges_df.to_excel(writer, sheet_name='edges', index=False)
