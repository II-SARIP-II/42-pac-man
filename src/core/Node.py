class Node():
    def __init__(self,
                 pos: tuple[int, int],
                 neighbours: list[tuple[int, int] | None],
                 wall: int
                 ) -> None:

        self.pos: tuple[int, int] = pos
        self.neighbours = neighbours
        self.wall = wall

        self.get_walls()

    def get_neighbour(self, direction: int) -> tuple[int, int] | None:
        return self.neighbours[direction]

    def get_walls(self) -> None:
        binary = format(self.wall, '04b')[::-1]

        for i, b in enumerate(binary[:len(self.neighbours)]):
            if b == '1':
                self.neighbours[i] = None

    def __repr__(self) -> str:
        return f"Node {self.pos}"
