from ursina import Entity, Vec3, color
from src.utils import convertPosToVec
from src.core.Node import Node
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Character(Entity):
    def __init__(
        self,
        model: str,
        width: int,
        height: int,
        parent: "GameScene",
        scale: Vec3 = Vec3(0.5, 0.5, 0.5),
        collider: str = "box",
        position: Vec3 = Vec3(0, 0, 0),
        color: color = color.yellow
    ):
        super().__init__(
            model=model,
            scale=Vec3(0.5, 0.5, 0.5),
            collider="box",
            position=Vec3(0, 0, 0),
            parent=parent,
            color=color,
        )

        self.size = width, height
        self.game_scene = parent

        self.position = convertPosToVec((0, 0), self.size)

        self.current_node = self.getNode((0, 0))
        self.target_node = self.current_node
        self.speed = 5.0
        self.wish_direction: int = -1
        self.current_direction: int = self.wish_direction

    def move(self, direction: str) -> None:
        pass

    def resetPos(self) -> None:
        pass

    def respawn(self) -> None:
        pass

    def die(self) -> None:
        pass

    def update(self) -> None:
        pass

    def getNode(self, coo: tuple[int, int]) -> Node:
        return self.game_scene.level.level_map[coo]
