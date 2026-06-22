from ..mazegenerator import MazeGenerator
from .Level import Level
from ..models.config import LevelValidation
from .Node import Node

class LevelGenerator():
    def generate_level(self, level: LevelValidation) -> Level:
        width = level.width
        height = level.height

        maze = MazeGenerator(size=(width, height))
        maze.generate()

        nodes = {}
        for y, row in enumerate(maze.maze):
            for x, cell in enumerate(row):
                pos = x, y
                nodes[pos] = Node(
                    pos=pos,
                    neighbours=self.get_neighbours(pos,
                        height, width),
                    wall=cell
                )
        return Level(height=height, width=width, level_map=nodes)

    def get_neighbours(self, pos: tuple[int, int],
        height: int, width: int) -> list[tuple[int, int] | None]:

        x, y = pos

        if y - 1 >= 0:
            north = (x, y - 1)
        else:
            north = None

        if x + 1 < width:
            est = (x + 1, y)
        else:
            est = None

        if y + 1 < height:
            south = (x, y + 1)
        else:
            south = None

        if x - 1 >= 0:
            west = (x - 1, y)
        else:
            west = None

        return [north, est, south, west]

if __name__ == "__main__":
    lvl1_val = LevelValidation(width=6, height=6)
    gen = LevelGenerator()

    lvl1 = gen.generate_level(lvl1_val)
    x = lvl1.level_map[(0, 0)].neighbours[1]
    if x:
        print(lvl1.level_map[x].neighbours)
