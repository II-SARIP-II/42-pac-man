from src.core.Item import Item


class Node:
    def __init__(
        self,
        pos: tuple[int, int],
        neighbours: list[tuple[int, int] | None],
        wall: int,
        size: tuple[int, int]
    ) -> None:

        self.pos: tuple[int, int] = pos
        self.neighbours = neighbours
        self.wall = wall
        self.size = size
        self.nb_neighbours = 0
        self.item: Item | None = None

        self.getWalls()
        self.getNbNeighbours()

    def getNeighbour(self, direction: int) -> tuple[int, int] | None:
        return self.neighbours[direction]

    def getWalls(self) -> None:
        binary = format(self.wall, "04b")[::-1]

        for i, b in enumerate(binary[: len(self.neighbours)]):
            if b == "1":
                self.neighbours[i] = None

    def getNbNeighbours(self) -> None:
        res = 0
        for n in self.neighbours:
            if n is not None:
                res += 1

        self.nb_neighbours = res

    def __repr__(self) -> str:
        return f"Node {self.pos}"
