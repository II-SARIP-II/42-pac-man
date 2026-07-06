import random
from enum import Enum
from typing import Optional, Tuple, Any, List

from ursina import Vec3, color

from src.core.Character import Character
from src.core.Node import Node
from src.core.Player import Player
from src.utils import convertVecToPos

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class EnumMode(Enum):
    CHASE = 1
    RANDOM = 2
    SCARED = 3
    DEAD = 4


class Ghost(Character):
    def __init__(
        self,
        width: int,
        height: int,
        parent: "GameScene",
        player: Player,
        position: Vec3,
        color: color = color.white,
    ) -> None:
        super().__init__(
            model="sphere",
            width=width,
            height=height,
            parent=parent,
            color=color,
            position=position,
        )
        self.width = width
        self.height = height
        self.is_edible = False
        self.player = player
        self.frame_counter = 0
        self.speed = 4
        self.last_node: Optional[Node] = None
        self.mode = EnumMode.CHASE
        self.chase_count = 0
        self.target_path: List[Node] = []

    def update(self) -> None:
        pass

    def getEaten(self) -> None:
        pass

    def getTargetPos(self) -> Vec3:
        return self.player.getPlayerPos()

    def chaseMovement(
            self,
            player_grid_pos: Tuple[int, int]
            ) -> Tuple[int, int]:
        pass

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
        player_vec = self.getTargetPos()
        player_pos_x, player_pos_y = convertVecToPos(
            player_vec,
            (self.width, self.height)
            )
        target_pos_x = abs(self.width // 2 - player_pos_x)
        target_pos_y = abs(self.height // 2 - player_pos_y)
        escape_pos = (target_pos_x, target_pos_y)
        if len(self.target_path) <= 1:
            self.mode = EnumMode.CHASE
            self.speed = 4
            self.chase_count = 0
        return escape_pos
