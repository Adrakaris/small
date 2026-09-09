
from enum import Enum

class Tile(Enum):
    SPACE = " "
    WALL = "#"
    PLAYER = "P"
    GOAL = "O"

MazeGrid = list[list[Tile]]
Coord = tuple[int, int]

class Maze:
    def __init__(self, size:Coord, goal_location:Coord, start_location:Coord) -> None:
        """
        type Coord = tuple[int, int]
        
        size: (width, height)
        goal_location: (x, y)
        start_location: (x, y)
        """
        self.size = size
        self.goal_location = goal_location
        self.start_location = start_location
        self.maze:MazeGrid = []

        self.generate()

    def generate(self):
        """
        Generates a maze
        """

        # 1. create a list of size size[0], size[1] of all WALLs
        x, y = self.size
        maze = [[Tile.WALL for _ in range(x)] for _ in range(y)]

        maze[1][1] = Tile.SPACE
        path = []

    def possible_moves(self, maze:MazeGrid, at:Coord, path:list[Coord]) -> list[Coord]:
        """
        GIVEN a maze, the current position, the current path,
        Return coordinates of all wall tiles which:
            - are NOT on the edge of the maze
            - are NOT adjacent to another path except the one we are already at
        From the current position

        :return: all coordinates of walls we can carve out
        """

        directions = [
            (at[0]-1, at[1]),
            (at[0]+1, at[1]),
            (at[0], at[1]-1),
            (at[0], at[1]+1)
        ]

        valid_directions:list[Coord] = []

        for x, y in directions:
            # if it is valid
            # add it to valid_directions
            ...

        return valid_directions
        
    def get(self, coord:Coord) -> Tile:
        """Given an (x,y) coordinate, gets the tile from the maze"""
        return self.maze[coord[1]][coord[0]]  # maze[y, x]
