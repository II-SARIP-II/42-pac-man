from typing import TYPE_CHECKING

from ursina import Vec3, color, time

from src.core.Item import Item

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class PacGum(Item):
    def __init__(
        self,
        score: int,
        position: Vec3,
        parent: "GameScene"
    ) -> None:

        super().__init__(
            score=score,
            position=position,
            parent=parent,
            scale=Vec3(0.2, 0.2, 0.2)
        )


class SuperPacGum(Item):
    def __init__(
        self,
        score: int,
        position: Vec3,
        parent: "GameScene"
    ) -> None:

        super().__init__(
            score=score,
            position=position,
            parent=parent,
            scale=Vec3(0.4, 0.4, 0.4)
        )

        self.flashing = 0
        self.speed = 0.1
        self.chrono = 0

    def update(self) -> None:
        self.chrono += time.dt

        if self.chrono >= self.speed:
            if self.flashing == 0:
                self.color = color.black
                self.flashing = 1
            else:
                self.color = color.salmon
                self.flashing = 0

            self.chrono = 0
