from src.core.Item import Item


class Node:
    """A single cell of the maze graph,
    with neighbours and an optional item."""

    def __init__(
        self,
        pos: tuple[int, int],
        neighbours: list[tuple[int, int] | None],
        wall: int,
        size: tuple[int, int]
    ) -> None:
        """Initialize the node and resolve its accessible neighbours.

        Args:
            pos (tuple[int, int]): Grid coordinate of this node.
            neighbours (list[tuple[int, int] | None]): Candidate
                neighbour coordinates, before wall pruning.
            wall (int): Bitmask of blocked cardinal directions.
            size (tuple[int, int]): Level grid dimensions.

        Returns:
            None.
        """
        self.pos: tuple[int, int] = pos
        self.neighbours = neighbours
        self.wall = wall
        self.size = size
        self.nb_neighbours = 0
        self.item: Item | None = None

        self.getWalls()
        self.getNbNeighbours()

    def getNeighbour(self, direction: int) -> tuple[int, int] | None:
        """Get the neighbour coordinate in a given direction.

        Args:
            direction (int): 0=north, 1=east, 2=south, 3=west.

        Returns:
            tuple[int, int] | None: The neighbour, or None if blocked.
        """
        return self.neighbours[direction]

    def getWalls(self) -> None:
        """Prune neighbours blocked by a wall according to `self.wall`.

        Returns:
            None.
        """
        binary = format(self.wall, "04b")[::-1]

        for i, b in enumerate(binary[: len(self.neighbours)]):
            if b == "1":
                self.neighbours[i] = None

    def getNbNeighbours(self) -> None:
        """Count and store the number of accessible neighbours.

        Returns:
            None.
        """
        res = 0
        for n in self.neighbours:
            if n is not None:
                res += 1

        self.nb_neighbours = res

    def __repr__(self) -> str:
        """Return a debug-friendly string representation.

        Returns:
            str: The node's grid position.
        """
        return f"Node {self.pos}"
