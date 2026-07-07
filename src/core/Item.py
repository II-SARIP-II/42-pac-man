from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Item(Entity):
    def __init__(
        self,
        score: int,
        position: Vec3,
        parent: "GameScene",
        model: str = "sphere",
        scale: Vec3 = Vec3(0.5, 0.5, 0.5),
        collider: str = 'box',
        color: color = color.salmon
    ) -> None:

        super().__init__(
            model=model,
            scale=scale,
            collider=collider,
            position=position,
            parent=parent,
            color=color
        )

        self.score = score
        self.pos = position
