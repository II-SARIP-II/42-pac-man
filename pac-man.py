from src.mazegenerator import MazeGenerator
from src.core.Node import Node


def main() -> None:
    size = 15

    maze = MazeGenerator()
    maze.generate()

    nodes = []
    for y, row in enumerate(maze.maze):
        for x, cell in enumerate(row):
            nodes.append(Node(
                id= y * 10 + x,
                pos=(x, y),
                neighbours=[]
            ))

if __name__ == "__main__":
    main()
