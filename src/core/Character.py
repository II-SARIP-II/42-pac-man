from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.core.Node import Node

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Character(Entity):
    def __init__(
        self,
        model: str,
        width: int,
        height: int,
        parent: "GameScene",
        texture: str | None,
        scale: Vec3 = Vec3(0.5, 0.5, 0.5),
        collider: str = "box",
        position: Vec3 = Vec3(0, 0, 0),
        color: color = color.yellow,
    ) -> None:
        super().__init__(
            model=model,
            scale=scale,
            collider="box",
            position=position,
            texture=texture,
            parent=parent,
            color=color,
        )

        self.size = width, height
        self.game_scene = parent

        self.position = position

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
