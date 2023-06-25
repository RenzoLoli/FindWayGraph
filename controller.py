from edges import Edge
from logger import Logger
from gui.gui import Window
from typing import List

class Controller:
    def __init__(self) -> None:
        self.gui = Window()
        Logger.set_logger(self.gui.get_logger())

    # def find_path(self, src: str, dst: str) -> List[Edge]:
    #     path = self.graph.path_finding(src, dst)
    #     return self.graph.osmids_to_edges(path)

    def run(self) -> None:
        self.gui.run()
