from typing import Callable, Dict, Iterator


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


class Edges:
    def __init__(self) -> None:
        self.edges = list()
        self.attrs = dict()

    def add_edge(self, edge: Edge) -> None:
        self.edges.append((edge.u, edge.v))
        self.attrs[f"{edge.u}-{edge.v}"] = edge

    def itter_u(self) -> Iterator[str]:
        return map(lambda ed: ed[0], self.edges)

    def itter_v(self) -> Iterator[str]:
        return map(lambda ed: ed[1], self.edges)
