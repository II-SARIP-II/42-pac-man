from ..mazegenerator import MazeGenerator
from ..models.config import LevelValidation
from .Level import Level
from .Node import Node


class LevelGenerator:
    """Builds `Level` instances from configuration using `MazeGenerator`."""

    def __init__(self, seed: int) -> None:
        """Initialize the generator with a seed for the first level.

        Args:
            seed (int): Seed for the first generated maze.

        Returns:
            None.
        """
        self.seed = seed
        self.seeded = False

    def generateLevel(self, level: LevelValidation) -> Level:
        """Generate a `Level` from the given level configuration.

        Args:
            level (LevelValidation): Width/height configuration.

        Returns:
            Level: The newly generated level.
        """
        width = level.width
        height = level.height

        if self.seeded:
            maze = MazeGenerator(size=(width, height))
        else:
            maze = MazeGenerator(size=(width, height), seed=self.seed)
            self.seeded = True

        nodes = {}
        for y, row in enumerate(maze.maze):
            for x, cell in enumerate(row):
                pos = x, y
                nodes[pos] = Node(
                    pos=pos,
                    neighbours=self.getNeighbours(pos, height, width),
                    wall=cell,
                    size=(width, height)
                )
        return Level(height=height, width=width, level_map=nodes)

    def getNeighbours(
        self, pos: tuple[int, int], height: int, width: int
    ) -> list[tuple[int, int] | None]:
        """Compute a cell's cardinal neighbour coordinates.

        Args:
            pos (tuple[int, int]): Grid coordinate to compute for.
            height (int): Level grid height.
            width (int): Level grid width.

        Returns:
            list[tuple[int, int] | None]: [north, east, south, west]
            coordinates, None where out of bounds.
        """
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
