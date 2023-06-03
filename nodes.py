from typing import Dict, Iterator, List, Tuple


class Node:
    def __init__(
        self,
        _osmid: str,
        _y: float,
        _x: float,
        _street_count: str,
        _highway: str,
        _geometry: str,
    ) -> None:
        self.osmid = _osmid
        self.street_count = _street_count
        self.highway = _highway
        self.geometry = _geometry
        self.y = _y
        self.x = _x

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
        self.attrs = dict()

    def to_list(self) -> List[str]:
        return self.nodes

    def iter(self) -> Iterator[str]:
        return iter(self.nodes)

    def iter_enumerate(self) -> Iterator[Tuple[int, str]]:
        return enumerate(self.nodes)

    def iter_attr(self) -> Iterator[Tuple[int, dict]]:
        return enumerate(list(map(lambda node: self.attrs[node], self.nodes)))

    def get_attr(self, osmid: str) -> Dict:
        return self.attrs[osmid]

    def add_node(self, node: Node) -> None:
        self.nodes.append(node.osmid)
        self.attrs[node.osmid] = node
