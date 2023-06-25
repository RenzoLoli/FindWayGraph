from typing import List, Tuple


class Route:
    def __init__(self, src_osmid: str, dst_osmid: str, algorithm: str):
        self.src_osmid = src_osmid
        self.dst_osmid = dst_osmid
        self.algorithm = algorithm
        self.path: List[List[Tuple[float, float]]] = []

    def clone(self):
        return Route(self.src_osmid, self.dst_osmid, self.algorithm)
    
    def copy(self, route):
        self.src_osmid = route.src_osmid
        self.dst_osmid = route.dst_osmid
        self.algorithm = route.algorithm

    def is_valid(self) -> bool:
        has_src = self.src_osmid is not None and self.src_osmid != ""
        has_dst = self.dst_osmid is not None and self.dst_osmid != ""
        has_algorithm = self.algorithm is not None and self.algorithm!= ""
        return has_src and has_dst and has_algorithm
    
    def clear(self):
        self.src_osmid = ""
        self.dst_osmid = ""
        self.algorithm = ""
        self.path = []
    
class Routes:
    def __init__(self):
        self.routes: List[Route] = []
    
    def new(self, route: Route):
        n_route = route.clone()
        self.routes.append(n_route)
        return n_route

    def update(self, id: int, route: Route):
        self.routes[id] = route

    def delete(self, id: int):
        del self.routes[id]

    def get(self, id: int):
        return self.routes[id]

    def clear(self):
        self.routes = []

    def as_list(self) -> list[Route]:
        return self.routes
    
    def empty(self):
        return len(self.routes) == 0