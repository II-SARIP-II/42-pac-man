from typing import TYPE_CHECKING, Any, Optional, Tuple

from ursina import time

from src.core.Ghost import EnumMode, Ghost
from src.core.Level import Level
from src.core.Node import Node
from src.core.Player import Player
from src.utils import convertPosToVec

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Blinky(Ghost):
    """Red ghost that chases the player's current position directly."""

    def __init__(
        self,
        width: int,
        height: int,
        parent: "GameScene",
        player: Player,
        level: Level
    ):
        """Create Blinky at the bottom-right spawn corner.

        Args:
            width (int): Level grid width.
            height (int): Level grid height.
            parent (GameScene): Scene to parent this ghost to.
            player (Player): Player to chase.
            level (Level): Level to navigate.

        Returns:
            None.
        """
        self.pos = (width - 1, height - 1)
        super().__init__(
            width=width,
            height=height,
            parent=parent,
            image_path="/assets/images/blinky.png",
            player=player,
            position=convertPosToVec(self.pos, (width, height)),
            level=level,
            spawn_pos=self.pos
        )

    def chaseMovement(
            self,
            player_grid_pos: Tuple[int, Any]
            ) -> Tuple[int, int]:
        """Compute the chase target: the player's current tile.

        Args:
            player_grid_pos (Tuple[int, Any]): Player's grid position.

        Returns:
            Tuple[int, int]: Target grid position (the player's tile).
        """
        self.alpha = 1
        self.chase_count += 1
        if self.chase_count > 20:
            self.mode = EnumMode.RANDOM
            self.speed = 2.5
            self.chase_count = 0
        return player_grid_pos

    def deadMovement(self) -> Any:
        """Get the target position while dead.

        Returns:
            Any: Spawn grid position.
        """
        return self.pos

    def moving(self) -> bool:
        """Advance one step along the current target path.

        Returns:
            bool: True if the next path node was reached this frame.
        """
        if len(self.target_path) < 2:
            return False
        target_vec = convertPosToVec(
            self.target_path[1].pos,
            (self.width, self.height)
        )
        vector_to_target = target_vec - self.position
        if vector_to_target:
            distance_left = vector_to_target.length()
            step = self.speed * time.dt
            if distance_left <= step:
                self.position = target_vec
                return True
            else:
                direction = vector_to_target.normalized()
                self.position += direction * step
                return False
        return False

    def bfs(
        self,
        start: Node,
        goal: Node,
        disallowed_node: Optional[Node] = None
    ) -> None:
        """Find the shortest path from `start` to `goal`.

        Args:
            start (Node): Ghost's current node.
            goal (Node): Target node.
            disallowed_node (Optional[Node]): Node to avoid revisiting.

        Returns:
            None.
        """
        if start == goal:
            self.target_path = [start]
            if self.mode == EnumMode.RANDOM:
                self.mode = EnumMode.CHASE
            else:
                self.mode = EnumMode.RANDOM
            return

        queue = [(start, [start])]
        visited = {start}

        if disallowed_node and disallowed_node != goal:
            if len(start.neighbours) > 1:
                visited.add(disallowed_node)

        while queue:
            current_node, path = queue.pop(0)
            for neighbor_pos in current_node.neighbours:
                if neighbor_pos is None:
                    continue
                neighbor_node = self.level.level_map[neighbor_pos]
                if neighbor_node not in visited:
                    new_path = path + [neighbor_node]
                    if neighbor_node == goal:
                        self.target_path = new_path
                        return
                    visited.add(neighbor_node)
                    queue.append((neighbor_node, new_path))

        self.target_path = []
