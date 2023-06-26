from logger import Logger
from nodes import  Node
from edges import  Edge

from viewer import GraphViewerStrattegy
from typing import Callable, List, Tuple, Dict

import math
import heapq

class Graph:
    def __init__(self, viewer_strattegy: GraphViewerStrattegy) -> None:
        self.graph: Dict[str, List[Tuple[str, float]]] = {}
        self.viewer: GraphViewerStrattegy = viewer_strattegy
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}

    @staticmethod
    def get_algorithms()-> List[str]:
        return ["A* v1", "A* v2", "A* v3", "Dijkstra v1", "Dijkstra v2"]

    def clear(self):
        self.graph.clear()
        self.viewer.clear()
        self.nodes.clear()
        self.edges.clear()

    def sort_nodes(self) -> None:
        self.nodes = {k: v for k, v in sorted(self.nodes.items(), key=lambda item: item[1].distance_to((0, 0)))}
        Logger.info(f"Sorted nodes!!")

    def calc_nearest_node(self, coord: Tuple[float, float]) -> Node | None:
        distance = float("inf")
        nearest_node = None
        Logger.info(f"Initial -> {coord}")
        for node in self.nodes.values():
            curr_distance = node.distance_to(coord)
            if curr_distance < distance:
                distance = curr_distance
                nearest_node = node

        if nearest_node:    Logger.info(f"Dest -> {nearest_node.to_coords()}")
        return nearest_node
    
    def get_node(self, osmid: str) -> Node:
        return self.nodes[osmid]
    
    def get_edge(self, u: str, v: str) -> Edge:
        return self.edges[f"{u},{v}"]

    def get_nodes(self) -> List[Node]:
        return list(self.nodes.values())
    
    def get_edges(self) -> List[Edge]:
        return list(self.edges.values())# type: ignore

    def get_nodes_osmid(self) -> List[str]:
        return list(self.nodes.keys())

    def build_viewer(self):
        self.viewer.clear()
        for _, node in self.nodes.items():
            self.viewer.add_node(node)

        for _, edge in self.edges.items():
            self.viewer.add_edge(edge)

    def add_node(self, node: Node) -> None:
        self.graph[node.osmid] = []
        self.nodes[node.osmid] = node

    def add_edge(self, edge: Edge) -> None:
        self.graph[edge.u].append((edge.v, edge.length))
        self.edges[f'{edge.u},{edge.v}'] = edge

    def distance_into(self, src: str, dst: str) -> float:
        # HEURISTICA
        # LA DISTANCIA ENTRE ARISTAS ES EL LENGTH
        # LA DISTANCIA QUE NO TIENE ARISTA ES LA DISTANCIA ENTRE LATITUD Y LONGITUD
        if src == dst: return 0
            
        edge_label = f'{src},{dst}'
        if edge_label in self.edges: return self.edges[edge_label].length

        src_node = self.nodes[src] 
        srcx, srcy = [src_node.x, src_node.y]

        dst_node = self.nodes[src]
        dstx, dsty = [dst_node.x, dst_node.y]

        def distance(lat1, lon1, lat2, lon2):
            R = 6378.137 # Radio de la tierra
            dlat = lat2 * math.pi / 180 - lat1 * math.pi / 180
            dlon = lon2 * math.pi / 180 - lon1 * math.pi / 180
            a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dlon/2) * math.sin(dlon/2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            d = R * c
            return d * 1000

        return distance(srcx, srcy, dstx, dsty)

    def osmids_to_nodes(self, osmids: List[str]) -> List[Node]:
        return list(map(lambda osmid: self.nodes[osmid], osmids))
    
    def osmids_to_edges(self, osmids: List[str]) -> List[Edge]:
        routes = []
        for [indx, osmid] in enumerate(osmids[:-1]):
            routes.append(self.edges[f'{osmid},{osmids[indx+1]}'])
        return routes

    def path_finding_v1(self, start: str, goal: str) -> List[str]:
        # MEJORAAAAAAAAAAAAAR
        open_set = []
        heapq.heapify(open_set)
        heapq.heappush(open_set, (0, start))
        came_from = {}
        max_distance = self.distance_into(start, goal)
        g_score = {start: 0.0}
        f_score = {start: max_distance}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal:
                # refactorizar el camino
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            for neighbor, _ in self.graph[current]:
                edge = self.edges[f'{current},{neighbor}']
                distance = self.distance_into(current, neighbor)
                current_g_score = g_score[current] + distance 
                current_g_score -= int(edge.highway == "secondary") * distance / 10
                
                if neighbor not in g_score or current_g_score < g_score[neighbor]:
                    # Encontramos un camino mejor hacia el vecino
                    came_from[neighbor] = current
                    g_score[neighbor] = current_g_score
                    f_score[neighbor] = current_g_score + self.distance_into(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # No se pudo encontrar un camino
        Logger.error("No existe camino para dicho lugar")
        return []
    
    def path_finding_v2(self, start: str, goal: str) -> List[str]:
        open_set = []
        closed_set = {}
        heapq.heapify(open_set)
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0.0}
        f_score = {start: self.distance_into(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)
            closed_set[current] = True

            if current == goal:
                # refactorizar el camino
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
        
            for neighbor, _ in self.graph[current]:
                #ayuda en eficiencia
                if neighbor in closed_set:
                    continue

                edge = self.edges[f'{current},{neighbor}']
                distance = self.distance_into(current, neighbor)
                curr_g_score = g_score[current] + distance
                curr_g_score -= int(edge.highway == "secondary") * distance / 10

                if neighbor not in g_score or curr_g_score < g_score[neighbor]:
                    came_from[neighbor] = current

                    g_score[neighbor] = curr_g_score
                    h_score = self.distance_into(neighbor, goal)
                    f_score[neighbor] = g_score[neighbor] + h_score
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        Logger.error("No existe camino para dicho lugar")
        return []

    def path_finding_v3(self, start: str, goal: str) -> List[str]:
        open_set = []
        heapq.heapify(open_set)
        heapq.heappush(open_set, (0, start))
        cameFrom = {}
        g_score = {key: math.inf for key in self.nodes.keys()}
        g_score[start] = 0
        f_score = {key: math.inf for key in self.nodes.keys()}
        f_score[start] = self.distance_into(start, goal)

        while open_set:
            current = heapq.heappop(open_set)[1]
            if current == goal:
                # refactorizar el camino
                path = []
                while current in cameFrom:
                    path.append(current)
                    current = cameFrom[current]
                path.append(start)
                path.reverse()
                return path
            
            for neighbor, _ in self.graph[current]:

                edge = self.edges[f'{current},{neighbor}']
                distance = self.distance_into(current, neighbor)
                curr_g_score = g_score[current] + distance
                curr_g_score -= int(edge.highway == "secondary") * distance / 10
                
                if curr_g_score < g_score[neighbor]:
                    cameFrom[neighbor] = current
                    g_score[neighbor] = curr_g_score
                    f_score[neighbor] = g_score[neighbor] + self.distance_into(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        Logger.error("No existe camino para dicho lugar")
        return []

    def dijkstra_v1(self, start: str, goal: str) -> List[str]:
        queue = []
        heapq.heapify(queue)
        heapq.heappush(queue, (0, start))
        came_from = {}
        g_score = {node: math.inf for node in self.nodes.keys()}
        visited = {node: False for node in self.nodes.keys()}

        while queue:
            curr_g_score, current = heapq.heappop(queue)
            
            if current == goal:
                # refactorizar el camino
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            if not visited[current]:
                visited[current] = True
                for neighbor, _ in self.graph[current]:
                    if not visited[neighbor]:
                        edge = self.get_edge(current, neighbor)
                        distance = self.distance_into(current, neighbor)
                        f_score = curr_g_score + distance
                        f_score -= int(edge.highway == "secondary") * distance / 10
                        if g_score[neighbor] > f_score:
                            came_from[neighbor] = current
                            g_score[neighbor] = f_score
                            heapq.heappush(queue, (f_score, neighbor))
                
        # No se pudo encontrar un camino
        Logger.error("No existe camino para dicho lugar")
        return []
    
    def dijkstra_v2(self, start: str, goal: str) -> List[str]:
        open_set = []
        heapq.heapify(open_set)
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {key: math.inf for key in self.nodes.keys()}
        visited = {key: False for key in self.nodes.keys()}

        while open_set:
            curr_score, current = heapq.heappop(open_set)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            visited[current] = True
            for neighbor, _ in self.graph[current]:
                if not visited[neighbor]:
                    edge = self.get_edge(current, neighbor)
                    distance = self.distance_into(current, neighbor)
                    curr_g_score = curr_score + distance
                    curr_g_score -= int(edge.highway == "secondary") * distance / 10
                    if g_score[neighbor] > curr_g_score:
                        g_score[neighbor] = curr_g_score
                        came_from[neighbor] = current
                        heapq.heappush(open_set, (curr_g_score, neighbor))
                
        Logger.error("No existe camino para dicho lugar")
        return []
    
    def choose_algorithm(self, algorithm: str) -> Callable[[str, str], List[str]]:
        if algorithm == "Dijkstra v1":
            return self.dijkstra_v1
        elif algorithm == "Dijkstra v2":
            return self.dijkstra_v2
        elif algorithm == "A* v1":
            return self.path_finding_v1
        elif algorithm == "A* v2":
            return self.path_finding_v2
        elif algorithm == "A* v3":
            return self.path_finding_v3
        else:
            return self.dijkstra_v1
        
    def plot_bytes(self) -> bytes:
        self.build_viewer()
        return self.viewer.pipe()
    
    def export(self) :
        Logger.info("exportando a imagen")
        self.build_viewer()
        self.viewer.export(directory="output", filename="plot", view=True)
        Logger.info("exportado")
