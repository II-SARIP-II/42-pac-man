from typing import TYPE_CHECKING, Optional, Tuple, Any

from ursina import color, time

from src.core.Ghost import EnumMode, Ghost
from src.core.Level import Level
from src.core.Node import Node
from src.core.Player import Player
from src.utils import convertPosToVec, convertVecToPos

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Clyde(Ghost):
    def __init__(
        self,
        width: int,
        height: int,
        parent: "GameScene",
        player: Player,
        level: Level
    ):
        if width % 2 != 0:
            self.pos = (width // 2, height // 2)
        else:
            self.pos = (width // 2 - 1, height // 2)
        self.basic_color = color.orange
        super().__init__(
            width=width,
            height=height,
            parent=parent,
            color=self.basic_color,
            player=player,
            position=convertPosToVec(self.pos, (width, height)),
        )
        self.level = level
        self.position = convertPosToVec(self.pos, (width, height))

    def update(self) -> None:
        if len(self.target_path) < 2:
            self.recalculate_path()

        arrive_au_node = self.moving()
        if arrive_au_node:
            if len(self.target_path) >= 2:
                self.last_node = self.target_path[0]
            self.recalculate_path()

    def chaseMovement(
            self,
            player_grid_pos: Tuple[int, Any]
            ) -> Tuple[int, int]:
        self.chase_count += 1
        if self.chase_count > 25:
            self.chase = EnumMode.RANDOM
            self.speed = 2.5
            self.chase_count = 0

        player_dir = self.player.current_direction
        add_pos = (0, 0)
        match player_dir:
            case 0:
                add_pos = (2, 0)
            case 1:
                add_pos = (0, -2)
            case 2:
                add_pos = (-2, 0)
            case 3:
                add_pos = (0, 2)
        return tuple(map(lambda x, y: x + y, player_grid_pos, add_pos))

    def recalculate_path(self) -> None:
        if self.mode == EnumMode.CHASE:
            player_pos = self.player.getPlayerPos()
            player_grid_pos = convertVecToPos(
                player_pos,
                (self.width, self.height)
            )
            target_pos = self.chaseMovement(player_grid_pos)
        elif self.mode == EnumMode.RANDOM:
            target_pos = self.randomMovement()
        else:
            target_pos = self.scaredMovement()
        ghost_grid_pos = convertVecToPos(
            self.position,
            (self.width, self.height)
        )

        if (
            ghost_grid_pos in self.level.level_map
            and target_pos in self.level.level_map
        ):
            self.bfs(
                self.level.level_map[ghost_grid_pos],
                self.level.level_map[target_pos],
                self.last_node,
            )
        else:
            self.bfs(
                self.level.level_map[ghost_grid_pos],
                self.level.level_map[player_grid_pos],
            )

    def moving(self) -> bool:
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
        if start == goal:
            self.target_path = [start]
            if self.mode == EnumMode.RANDOM:
                self.mode == EnumMode.CHASE
            else:
                self.mode == EnumMode.RANDOM
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
