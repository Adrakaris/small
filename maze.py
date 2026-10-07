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
    def __init__(self, size:Coord) -> None:
        """
        type Coord = tuple[int, int]
        
        size: (width, height)
        goal_location: (x, y)
        start_location: (x, y)
        """
        self.size = size
        self.maze:MazeGrid = []
        self.player_location = (1, 1)

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

        # 4. set a goal position
        possible_position = (x-2, y-2)
        if self.get(possible_position) == Tile.WALL:
            possible_position = (x-3, y-2)
        if self.get(possible_position) == Tile.WALL:
            possible_position = (x-2, y-3)
        if self.get(possible_position) == Tile.WALL:
            possible_position = (x-3, y-3)
        if self.get(possible_position) == Tile.WALL:
            raise ValueError(f"Cannot find a goal in this maze\n{self}")
        maze[possible_position[1]][possible_position[0]] = Tile.GOAL

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

    def player(self) -> Coord:
        """Returns the position of the player"""
        return self.player_location

    def move(self, x:int, y:int) -> bool:
        """
        Tries to move the player x spaces RIGHT and y spaces DOWN

        Returns False if this is not possible (e.g. a wall)
        """
        current_x, current_y = self.player_location
        
        if not (0 <= current_x + x <= self.size[0]):
            return False
        if not (0 <= current_y + y <= self.size[1]):
            return False
        if self.get((current_x + x, current_y + y)) == Tile.WALL:
            return False

        self.player_location = (current_x + x, current_y + y)
        return True

    def __repr__(self) -> str:
        return f"Maze size={self.size}\n" + "\n".join([
            "".join([tile.value if (x, y) != self.player_location else Tile.PLAYER.value for x, tile in enumerate(row) ])
            for y, row in enumerate(self.maze)
        ])



if __name__ == "__main__":
    maze = Maze((20, 20))
    print(maze)
    print()
    print(maze.move(1, 0))
    print(maze)
    print()
    print(maze.move(0, 1))
    print(maze)
