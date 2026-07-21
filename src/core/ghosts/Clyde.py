from typing import TYPE_CHECKING, Any, Optional, Tuple

from ursina import time

from src.core.Ghost import EnumMode, Ghost
from src.core.Level import Level
from src.core.Node import Node
from src.core.Player import Player
from src.utils import convertPosToVec
from src.utils_io import resource_path

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Clyde(Ghost):
    """Orange ghost that targets a tile offset behind the player."""

    def __init__(
        self,
        width: int,
        height: int,
        parent: "GameScene",
        player: Player,
        level: Level
    ):
        """Create Clyde at the bottom-left spawn corner.

        Args:
            width (int): Level grid width.
            height (int): Level grid height.
            parent (GameScene): Scene to parent this ghost to.
            player (Player): Player to chase.
            level (Level): Level to navigate.

        Returns:
            None.
        """
        self.pos = (0, 0)

        super().__init__(
            width=width,
            height=height,
            parent=parent,
            image_path=resource_path("/assets/images/clyde.png"),
            player=player,
            position=convertPosToVec(self.pos, (width, height)),
            level=level,
            spawn_pos=self.pos
        )

    def chaseMovement(
            self,
            player_grid_pos: Tuple[int, Any]
            ) -> Tuple[int, int]:
        """Compute the chase target: a tile offset behind the player.

        Args:
            player_grid_pos (Tuple[int, Any]): Player's grid position.

        Returns:
            Tuple[int, int]: Target grid position.
        """
        self.alpha = 1
        self.chase_count += 1
        if self.chase_count > 25:
            self.mode = EnumMode.RANDOM
            self.speed = 2.5
            self.chase_count = 0

        # Offset opposite to the player's facing direction (i.e. the
        # tile they just came from), matching "behind the player".
        player_dir = self.player.current_direction
        add_pos = (0, 0)
        match player_dir:
            case 0:
                add_pos = (0, 2)
            case 1:
                add_pos = (-2, 0)
            case 2:
                add_pos = (0, -2)
            case 3:
                add_pos = (2, 0)
        return tuple(map(lambda x, y: x + y, player_grid_pos, add_pos))

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

        If the ghost has already reached its target tile, alternates
        between CHASE and RANDOM for variety, or revives a DEAD ghost
        that reached its spawn tile. Leaves SCARED/STOP mode untouched.

        Args:
            start (Node): Ghost's current node.
            goal (Node): Target node.
            disallowed_node (Optional[Node]): Node to avoid revisiting.

        Returns:
            None.
        """
        if start == goal:
            self.target_path = [start]
            if self.mode == EnumMode.DEAD:
                self.mode = EnumMode.RANDOM
                self.speed = 2
                self.alpha = 1.0
            elif self.mode == EnumMode.RANDOM:
                self.mode = EnumMode.CHASE
                self.speed = 2
            elif self.mode == EnumMode.CHASE:
                self.mode = EnumMode.RANDOM
            return

        queue = [(start, [start])]
        visited = {start}

        if disallowed_node and disallowed_node != goal:
            if start.nb_neighbours > 1:
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
