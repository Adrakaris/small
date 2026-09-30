import random 
from enum import Enum

class Tile(Enum):
    SPACE = " "
    WALL = "█"
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
        # 2. use recursive backtracking to generate the maze
        self.walk_maze((1,1), maze)
        # 3. assign it to self
        self.maze = maze

    def walk_maze(self, position:Coord, maze:MazeGrid):
        # 1. get all possible moves
        # 2. 
        #   BASE CASE: no possible moves: set this position to a SPACE, and return 
        #   RECURSIVE CASE: there are possible moves:
        #       - set this position to SPACE,
        #       - for EACH possible move in a RANDOM order, walk_maze(new position)
        maze[position[1]][position[0]] = Tile.SPACE

        while len(moves := self.possible_moves(maze, position)) > 0:
            self.walk_maze(random.choice(moves), maze)

    def possible_moves(self, maze:MazeGrid, at:Coord) -> list[Coord]:
        """
        GIVEN a maze, the current position, the current path,
        Return coordinates of all wall tiles which:
            - are NOT on the edge of the maze
            - are NOT adjacent to another path except the one we are already at
        From the current position

        :return: all coordinates of walls we can carve out
        """

        directions = self.get_coordinates_around(at)
        
        valid_directions:list[Coord] = []

        for x, y in directions:
            # which cases is it invalid?
            # INVALID DUE TO EDGE
            # x = 0 or y = 0: left/top wall -> invalid
            if x == 0 or y == 0:
                continue
            # x = self.size[0]-1 or y = self.size[1]-1: right/bottom wall -> invalid 
            if x == self.size[0]-1 or y == self.size[1]-1:
                continue
            # invalid due to already being a path
            if maze[y][x] == Tile.SPACE:
                continue
            
            # INVALID DUE TO TOUCHING AN EXISTING PATH THAT'S NOT THE CURRENT POSITION
            #   get all the tiles around x, y
            #   EXCLUDE the `at` coordinate
            #   check that none are Tile.SPACE
            around = self.get_coordinates_around((x,y))
            invalid = False
            for x2, y2 in around:
                if (x2,y2) == at: 
                    continue
                if maze[y2][x2] == Tile.SPACE:
                    invalid = True
            if invalid:
                continue

            valid_directions.append((x, y))
        return valid_directions

    def get_coordinates_around(self, coord:Coord) -> list[Coord]:
        """gets the four orthogonally adjacent coordinates around a """
        return [
            (coord[0]-1, coord[1]),
            (coord[0]+1, coord[1]),
            (coord[0], coord[1]-1),
            (coord[0], coord[1]+1)
        ]
        
    def get(self, coord:Coord) -> Tile:
        """Given an (x,y) coordinate, gets the tile from the maze"""
        return self.maze[coord[1]][coord[0]]  # maze[y, x]

    def __repr__(self) -> str:
        return f"Maze size={self.size}\n" + "\n".join([
            "".join([tile.value for tile in row])
            for row in self.maze
        ])



if __name__ == "__main__":
    maze = Maze((10, 10), (1,1), (1,1))
    print(maze)
