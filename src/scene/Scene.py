from ursina import Entity, Vec3, color
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class Scene(Entity):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__()

        self.game_engine = game_engine

    def createScene(self) -> None:
        pass

    def createBackground(self) -> None:
        Entity(
            model="plane",
            scale=Vec3(20, 1, 20),
            position=Vec3(0, 0, 0),
            color=color.black,
            collider="box",
            parent=self,
        )

    def onEntry(self) -> None:
        self.enable()

    def onExit(self) -> None:
        self.disable()
