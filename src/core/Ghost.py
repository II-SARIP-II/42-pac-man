import random
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from ursina import Vec3, color

from src.core.Character import Character
from src.core.Node import Node
from src.core.Player import Player
from src.utils import convertVecToPos

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class EnumMode(Enum):
    CHASE = 1
    RANDOM = 2
    SCARED = 3
    DEAD = 4
    STOP = 5


class Ghost(Character):
    def __init__(
        self,
        width: int,
        height: int,
        image_path: str,
        parent: "GameScene",
        player: Player,
        position: Vec3,
    ) -> None:
        spawn_position = Vec3(position.x, 0.1, position.z)

        super().__init__(
            model="quad",
            texture=image_path,
            width=width,
            height=height,
            parent=parent,
            scale=Vec3(0.6, 0.6, 0.6),
            color=color.white,
            position=spawn_position,
        )
        self.rotation = Vec3(90, 0, 0)
        self.width = width
        self.height = height
        self.is_edible = False
        self.player = player
        self.frame_counter = 0
        self.speed = 2
        self.last_node: Optional[Node] = None
        self.mode = EnumMode.CHASE
        self.chase_count = 0
        self.target_path: List[Node] = []
        self.last_player_death = datetime.now()

    def update(self) -> None:
        pass

    def getEaten(self) -> None:
        pass

    def getTargetPos(self) -> Vec3:
        return self.player.getPlayerPos()

    def randomMovement(self) -> Tuple[int, int]:
        self.chase_count += 1
        if self.chase_count > 15:
            self.mode = EnumMode.CHASE
            self.speed = 4
            self.chase_count = 0
        return (
            random.randint(0, self.width - 1),
            random.randint(0, self.height - 1),
        )

    def scaredMovement(self) -> Any:
        self.texture = "assets/images/scared_ghost.png"

        player_vec = self.getTargetPos()
        player_x, player_y = convertVecToPos(player_vec, (self.width, self.height))
        ghost_grid_pos = convertVecToPos(self.position, (self.width, self.height))
        current_node = self.level.level_map[ghost_grid_pos]
        best_pos = ghost_grid_pos
        max_distance = -1

        for neighbour_pos in current_node.neighbours:
            if neighbour_pos is None:
                continue

            nx, ny = neighbour_pos
            distance = abs(player_x - nx) + abs(player_y - ny)

            if distance > max_distance:
                max_distance = distance
                best_pos = neighbour_pos

        print(best_pos)
        return best_pos

    def playerCollision(self) -> None:
        player_vec = self.getTargetPos()
        player_pos = convertVecToPos(
            player_vec,
            (self.width, self.height)
            )
        ghost_pos = convertVecToPos(
            self.position,
            (self.width, self.height)
            )
        grace_period = timedelta(seconds=5)
        if datetime.now() < self.last_player_death + grace_period:
            return
        if player_pos == ghost_pos:
            self.last_player_death = datetime.now()
            self.parent.killPlayer()
