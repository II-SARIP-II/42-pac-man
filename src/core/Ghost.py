from ursina import Vec3, color

from src.core.Character import Character
from src.core.Player import Player


class Ghost(Character):
    def __init__(
        self,
        width: int,
        height: int,
        parent: "GameScene",
        player: Player,
        position: Vec3,
        color=color.white,
    ) -> None:
        super().__init__(
            model="sphere",
            width=width,
            height=height,
            parent=parent,
            color=color,
            position=position,
        )
        self.is_edible = False
        self.player = player

    def behaviour(self) -> None:
        # the ghost's ia
        pass

    def update(self) -> None:
        pass

    def getEaten(self) -> None:
        # if the ghost is eaten
        pass

    def getTargetPos(self) -> Vec3:
        return self.player.getPlayerPos()
