class Node():
    def __init__(self, id, pos, neighbours) -> None:
        self.id = id
        self.pos: tuple[int, int] = pos
        self.walls = {
            'N': False,
            'E': False,
            'S': False,
            'W': False
        }
        self.neighbours = neighbours

    def __repr__(self) -> str:
        return f"Node {self.id}"
