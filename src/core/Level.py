from .Node import Node


class Level:
    """A single maze level: dimensions plus a graph of connected `Node`s."""

    def __init__(
        self, height: int, width: int, level_map: dict[tuple[int, int], Node]
    ) -> None:
        """Initialize the level with its dimensions and node graph.

        Args:
            height (int): Level grid height.
            width (int): Level grid width.
            level_map (dict[tuple[int, int], Node]): Grid-to-node mapping.

        Returns:
            None.
        """
        self.height = height
        self.width = width
        self._level_map = level_map

    @property
    def level_map(self) -> dict[tuple[int, int], Node]:
        """dict[tuple[int, int], Node]: The grid-to-node mapping."""
        return self._level_map
