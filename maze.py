
from enum import Enum

class Tile(Enum):
    SPACE = " "
    WALL = "#"
    PLAYER = "P"
    GOAL = "O"


class Maze:
    def __init__(self, size:tuple[int, int], goal_location:tuple[int, int], start_location:tuple[int, int]) -> None:
        """
        size: (width, height)
        goal_location: (x, y)
        start_location: (x, y)
        """
        self.size = size
        self.goal_location = goal_location
        self.start_location = start_location
        self.maze:list[list[Tile]] = []

        self.generate()

    def generate(self):
        """
        Generates a maze
        """

        # TODO do backtracking
        # #######
        # #O#d e#   O: (0, 0)
        # # # # #
        # #a c#b#   a: (0, 1) b: (0, 2)
        # #######
