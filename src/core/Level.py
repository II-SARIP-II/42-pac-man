from .Node import Node


class Level:
    def __init__(
        self, height: int, width: int, level_map: dict[tuple[int, int], Node]
    ) -> None:
        self.height = height
        self.width = width
        self._level_map = level_map

    @property
    def level_map(self) -> dict[tuple[int, int], Node]:
        return self._level_map
