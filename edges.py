from typing import Any, Dict, Iterator, List, Tuple, Set, Union

from nodes import Nodes


class Edge:
    def __init__(
        self,
        _u: str,
        _v: str,
        _oneway: bool,
        _name: str,
        _highway: str,
        _reversed: bool,
        _length: float,
        _geometry: str,
    ) -> None:
        self.u = _u
        self.v = _v
        self.oneway = _oneway
        self.name = _name
        self.highway = _highway
        self.reversed = _reversed
        self.length = _length
        self.geometry = _geometry
        self.weight = 0
        self.attrs = {"color": "black"}

    def __str__(self) -> str:
        txt = ""
        txt += f"u: {self.u}\n"
        txt += f"v: {self.v}\n"
        txt += f"oneway: {self.oneway}\n"
        txt += f"name: {self.name}\n"
        txt += f"highway: {self.highway}\n"
        txt += f"reversed: {self.reversed}\n"
        txt += f"length: {self.length}\n"
        txt += f"geometry: {self.geometry}\n"
        txt += f"weight: {self.weight}\n"
        return txt
    
    def default_attrs(self):
        self.attrs = {"color": "black"}

    def config_attrs(self, **attrs):
        self.attrs.update(attrs)

    def to_path(self) -> List[Tuple[float, float]]:
        normalized = self.geometry.replace("LINESTRING (", "")[:-1].split(",")
        splitted = [tuple(norm.strip().split(" ")) for norm in normalized ]
        return list(map(lambda sp: (float(sp[0]), float(sp[1])),splitted))
