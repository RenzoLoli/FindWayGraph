import math
from typing import Dict, Iterator, List, Tuple

from logger import Logger


class Node:
    def __init__(
        self,
        _osmid: str,
        _y: float,
        _x: float,
        _street_count: str,
        _highway: str,
        _geometry: str
    ) -> None:
        self.osmid = _osmid
        self.street_count = _street_count
        self.highway = _highway
        self.geometry = _geometry
        self.y = _y
        self.x = _x

    def to_coords(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    def distance_to(self, coord: Tuple[float, float]) -> float:
        return math.sqrt(math.pow(self.x - coord[0], 2) + math.pow(self.y - coord[1], 2))

    def __str__(self) -> str:
        txt = ""
        txt += "osmid: " + self.osmid
        txt += "street_count: " + self.street_count
        txt += "highway: " + self.highway
        txt += "(y, x): " + str((self.y, self.x))
        txt += "geometry: " + self.geometry
        return txt

class Nodes:
    def __init__(self) -> None:
        self.nodes = list()

    def find_index(self, value: str) -> int:
        return self.nodes.index(value)

    def to_list(self) -> List[str]:
        return self.nodes

    def get(self, index: int) -> str:
        return self.nodes[index]

    def iter(self) -> Iterator[str]:
        return iter(self.nodes)

    def iter_enumerate(self) -> Iterator[Tuple[int, str]]:
        return enumerate(self.nodes)

    def add_node(self, node: Node) -> None:
        self.nodes.append(node.osmid)
