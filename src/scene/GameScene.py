from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.core.Level import Level
from src.scene.EnumScene import EnumScene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class GameScene(Entity):
    def __init__(self, game_state: "GameEngine") -> None:
        super().__init__()

        self.game_state = game_state

    def input(self, key: str) -> None:
        if key == "escape":
            self.game_state.displayScene(EnumScene.MENU)
        if key == "p":
            self.game_state.displayScene(EnumScene.PAUSE)
        if key == "l":
            self.game_state.displayScene(EnumScene.LOSE)
        if key == "v":
            self.game_state.displayScene(EnumScene.WIN)

    def createMap(self, level: Level) -> None:
        Entity(
            model="plane",
            scale=Vec3(level.width, 0, level.height),
            position=Vec3(0, 0, 0),
            color=color.black,
            collider="box",
            parent=self,
        )
        Entity(
            model="plane",
            scale=Vec3(1, 0, 1),
            position=Vec3(0, 1, 0),
            color=color.yellow,
            collider="box",
            parent=self,
        )
        for node in level.levelMap.values():
            cell_x = node.pos[0] - (level.width / 2) + 0.5
            cell_z = -(node.pos[1] - (level.height / 2) + 0.5)
            if not node.getNeighbour(0):
                Entity(
                    model="cube",
                    scale=Vec3(1, 2, 0.1),
                    position=Vec3(cell_x, 0.5, cell_z + 0.5),
                    color=color.blue,
                    collider="box",
                    parent=self,
                )

            if not node.getNeighbour(1):
                Entity(
                    model="cube",
                    scale=Vec3(0.1, 2, 1),
                    position=Vec3(cell_x + 0.5, 0.5, cell_z),
                    color=color.blue,
                    collider="box",
                    parent=self,
                )

            if not node.getNeighbour(2):
                Entity(
                    model="cube",
                    scale=Vec3(1, 2, 0.1),
                    position=Vec3(cell_x, 0.5, cell_z - 0.5),
                    color=color.blue,
                    collider="box",
                    parent=self,
                )

            if not node.getNeighbour(3):
                Entity(
                    model="cube",
                    scale=Vec3(0.1, 2, 1),
                    position=Vec3(cell_x - 0.5, 0.5, cell_z),
                    color=color.blue,
                    collider="box",
                    parent=self,
                )
