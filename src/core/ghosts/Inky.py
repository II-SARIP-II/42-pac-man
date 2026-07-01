import time
from typing import TYPE_CHECKING, Optional

from ursina import Vec3, color

from src.core.Ghost import Ghost
from src.core.Level import Level
from src.core.Node import Node
from src.core.Player import Player
from src.utils import convertPosToVec, convertVecToPos

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Inky(Ghost):
    def __init__(
        self, width: int, height: int, parent: "GameScene", player: Player, level: Level
    ):
        self.pos = (width - 1, 0)
        super().__init__(
            width=width,
            height=height,
            parent=parent,
            color=color.cyan,
            player=player,
            position=convertPosToVec(self.pos, (width, height)),
        )
        self.level = level
        self.width = width
        self.height = height
        self.target_path = []
        self.position = convertPosToVec(self.pos, (width, height))
        self.frame_counter = 0
        self.speed = 4.5
        self.last_node: Optional[Node] = None

    def update(self) -> None:
        self.behaviour()

    def behaviour(self) -> None:
        if len(self.target_path) < 2:
            self.recalculate_path()

        arrive_au_node = self.move()
        if arrive_au_node:
            if len(self.target_path) >= 2:
                self.last_node = self.target_path[0]
            self.recalculate_path()

    def recalculate_path(self) -> None:
        player_pos = self.player.getPlayerPos()
        player_dir = self.player.current_direction
        add_pos = (0, 0)
        player_grid_pos = convertVecToPos(player_pos, (self.width, self.height))
        match player_dir:
            case 0:
                add_pos = (0, -2)
            case 1:
                add_pos = (2, 0)
            case 2:
                add_pos = (0, 2)
            case 3:
                add_pos = (-2, 0)
        target_node = tuple(map(lambda x, y: x + y, player_grid_pos, add_pos))
        ghost_grid_pos = convertVecToPos(self.position, (self.width, self.height))

        if (
            ghost_grid_pos in self.level.level_map
            and target_node in self.level.level_map
        ):
            self.bfs(
                self.level.level_map[ghost_grid_pos],
                self.level.level_map[target_node],
                self.last_node,
            )
        else:
            self.bfs(
                self.level.level_map[ghost_grid_pos],
                self.level.level_map[player_grid_pos],
            )

    def move(self) -> bool:
        """Déplace le fantôme et renvoie True s'il a atteint son nœud cible."""
        if len(self.target_path) < 2:
            return False
        target_vec = convertPosToVec(self.target_path[1].pos, (self.width, self.height))
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
        self, start: Node, goal: Node, disallowed_node: Optional[Node] = None
    ) -> None:
        if start == goal:
            self.target_path = [start]
            return

        queue = [(start, [start])]
        visited = {start}

        if disallowed_node and disallowed_node != goal:
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
