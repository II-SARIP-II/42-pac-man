from typing import TYPE_CHECKING, Optional, Tuple, Any

from ursina import color, time

from src.core.Ghost import EnumMode, Ghost
from src.core.Level import Level
from src.core.Node import Node
from src.core.Player import Player
from src.utils import convertPosToVec, convertVecToPos

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Blinky(Ghost):
    def __init__(
        self,
        width: int,
        height: int,
        parent: "GameScene",
        player: Player,
        level: Level
    ):
        self.pos = (width - 1, height - 1)
        self.basic_color = color.red
        super().__init__(
            width=width,
            height=height,
            parent=parent,
            color=self.basic_color,
            image_path="/assets/images/blinky.png",
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
        if self.chase_count > 20:
            self.mode = EnumMode.RANDOM
            self.speed = 2.5
            self.chase_count = 0
            self.color = self.basic_color
        return player_grid_pos

    def deadMovement(self) -> Any:
        return self.pos

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
        elif self.mode == EnumMode.SCARED:
            target_pos = self.scaredMovement()
        else:
            target_pos = self.deadMovement()

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
