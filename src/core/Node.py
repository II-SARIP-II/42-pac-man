class Node():
    def __init__(self, pos: tuple[int, int],
        neighbours: list[tuple[int, int] | None], wall: int) -> None:

        self.pos: tuple[int, int] = pos
        self.neighbours = neighbours

    def get_neighbour(self, direction: int) -> tuple[int, int] | None:
        return self.neighbours[direction]

    def __repr__(self) -> str:
        return f"Node {self.pos}"
