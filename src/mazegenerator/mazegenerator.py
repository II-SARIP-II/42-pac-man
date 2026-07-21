import random
from collections import deque
from typing import Iterator


class MazeGenerator:
    """Generates a random maze using a recursive-backtracker algorithm.

    Each cell is stored as a 4-bit wall bitmask (bit 0=north, 1=east,
    2=south, 3=west blocked).
    """

    def __init__(self, size: tuple[int, int] = (15, 15), perfect: bool = False,
                 entry_cell: tuple[int, int] = (0, 0),
                 exit_cell: tuple[int, int] = (-1, -1),
                 seed: int = 0) -> None:
        """Initialize and immediately generate a maze.

        Args:
            size (tuple[int, int]): Maze (width, height), in cells.
            perfect (bool): If True, no loops are added.
            entry_cell (tuple[int, int]): Maze entry cell.
            exit_cell (tuple[int, int]): Maze exit cell.
            seed (int): Random seed; 0 for non-deterministic.

        Returns:
            None.
        """
        self._width = size[0]
        self._height = size[1]
        self._perfect = perfect
        self._seed = seed
        self._entryx = (entry_cell[0]
                        if 0 <= entry_cell[0] < self._width else 0)
        self._entryy = (entry_cell[1]
                        if 0 <= entry_cell[1] < self._height else 0)
        self._exitx = (exit_cell[0]
                       if 0 <= exit_cell[0] < self._width else self._width-1)
        self._exity = (exit_cell[1]
                       if 0 <= exit_cell[1] < self._height else self._height-1)
        self._maze: list[list[int]] = []
        self._path: list[list[int]] = []
        self._shortest_path: str | bool = False
        self.generate(self._seed)
        return None

    @property
    def maze(self) -> list[list[int]]:
        """list[list[int]]: The generated maze as rows of wall bitmasks."""
        return self._maze

    @property
    def shortest_path(self) -> str | bool:
        """str | bool: Direction-letter path from entry to exit, or False."""
        return self._shortest_path

    @property
    def maze_entry(self) -> tuple[int, int]:
        """tuple[int, int]: The maze's entry cell."""
        return self._entryx, self._entryy

    @property
    def maze_exit(self) -> tuple[int, int]:
        """tuple[int, int]: The maze's exit cell."""
        return self._exitx, self._exity

    def generate(self, seed: int = 0) -> None:
        """Generate a new maze, replacing any previously generated one.

        Args:
            seed (int): Random seed; 0 for non-deterministic.

        Returns:
            None.
        """
        random.seed(seed) if seed > 0 else random.seed()
        self._seed = seed
        self._create_empty_maze()
        self._add_42_to_maze()
        self._generate_maze(self._entryx, self._entryy, 0)
        self._find_short_path()

#    Private functions

    def _create_empty_maze(self) -> None:
        """Build the initial grid with all cells open and a solid border.

        Returns:
            None.
        """
        self._maze = [[8] + [0] * (self._width-2) +
                      [2] for _ in range(self._height-2)]
        self._maze.insert(0, [9] + [1] * (self._width-2) + [3])
        self._maze.append([12] + [4] * (self._width-2) + [6])
        self._path = [[0] * self._width for _ in range(self._height)]

    def _add_42_to_maze(self) -> None:
        """Stamp a small "42" glyph pattern into the center of the maze.

        Returns:
            None.
        """
        ft_small = [[1, 0, 0, 0, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 0, 1, 1, 1],
                    [0, 0, 1, 0, 1, 0, 0],
                    [0, 0, 1, 0, 1, 1, 1]
                    ]
        if len(ft_small)*2 > self._height or len(ft_small[0])*2 > self._width:
            print("MazeGenerator Warning: maze is too small to add '42' in it")
            return
        posy = int((self._height - len(ft_small)) / 2)
        posx = int((self._width - len(ft_small[0])) / 2)
        for y in range(len(ft_small)):
            for x in range(len(ft_small[0])):
                if ft_small[y][x] == 1:
                    self._maze[posy+y][posx+x] = 15
                    self._maze[posy+y][posx+x-1] |= 2
                    self._maze[posy+y][posx+x+1] |= 8
                    self._maze[posy+y-1][posx+x] |= 4
                    self._maze[posy+y+1][posx+x] |= 1
                    self._path[posy+y][posx+x] = 1

    def _is_available(self, x: int, y: int) -> bool:
        """Check whether a cell is within bounds and not yet visited.

        Args:
            x (int): Column index.
            y (int): Row index.

        Returns:
            bool: True if the cell is in bounds and unvisited.
        """
        if (
                0 <= y < self._height and
                0 <= x < self._width and self._path[y][x] == 0
        ):
            return True
        return False

    def _get_neighbors(self, x: int,
                       y: int) -> Iterator[tuple[int, int, int, int]]:
        """Yield unvisited neighbours of a cell, in random order.

        Also has a 1-in-6 chance of knocking down a wall to an already
        visited neighbour, adding loops when `self._perfect` is False.

        Args:
            x (int): Column index.
            y (int): Row index.

        Yields:
            tuple[int, int, int, int]: Neighbour (x, y), the wall bit to
            it, and the opposite wall bit back.
        """
        directions = [(1, 0, 2, 8), (-1, 0, 8, 2), (0, 1, 4, 1), (0, -1, 1, 4)]
        random.shuffle(directions)
        for dw, dh, code, opp_code in directions:
            nx, ny = x + dw, y + dh
            if self._is_available(nx, ny):
                yield nx, ny, code, opp_code
            else:
                if (
                        self._perfect is False and random.randint(0, 5) == 0
                        and 0 <= ny < self._height and 0 <= nx < self._width
                ):
                    if (
                            self._maze[ny][nx] != 15 and
                            (self._maze[y][x] & (~code)) != 0 and
                            (self._maze[ny][nx] & (~opp_code)) != 0
                    ):
                        self._maze[y][x] = self._maze[y][x] & (~code)
                        self._maze[ny][nx] = self._maze[ny][nx] & (~opp_code)

    def _generate_maze(self, x: int, y: int, from_code: int) -> None:
        """Recursively carve the maze via depth-first backtracking.

        Args:
            x (int): Column index.
            y (int): Row index.
            from_code (int): Wall bit this cell was entered from.

        Returns:
            None.
        """
        self._path[y][x] = 1
        non_mutable = self._maze[y][x]
        self._maze[y][x] = 15 & ~from_code
        for nx, ny, code, opp_code in self._get_neighbors(x, y):
            if code & non_mutable:
                continue
            self._maze[y][x] = self._maze[y][x] & (~code)
            self._generate_maze(nx, ny, opp_code)

    def _find_short_path(self) -> None:
        """Compute the shortest path from the entry cell to the exit cell.

        Returns:
            None.
        """
        directions = [(0, 1, 4, 'S'), (1, 0, 2, 'E'),
                      (-1, 0, 8, 'W'), (0, -1, 1, 'N')]
        if (self._entryx, self._entryy) == (self._exitx, self._exity):
            self._shortest_path = ''
            return
        visited = [[False] * self._width for _ in range(self._height)]
        visited[self._entryy][self._entryx] = True
        queue: deque[tuple[int, int, str]] = deque(
            [(self._entryx, self._entryy, '')])
        while queue:
            x, y, ways = queue.popleft()
            for dx, dy, code, way in directions:
                if (self._maze[y][x] & code) != 0:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < self._width and 0 <= ny < self._height):
                    continue
                if visited[ny][nx]:
                    continue
                if (nx, ny) == (self._exitx, self._exity):
                    self._shortest_path = ways + way
                    return
                visited[ny][nx] = True
                queue.append((nx, ny, ways + way))
        print("MazeGenerator Class error: no shortest path found.")
        return
