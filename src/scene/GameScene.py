from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.core.Level import Level
from src.core.Player import Player
from src.scene.EnumScene import EnumScene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class GameScene(Entity):
    def __init__(self, game_state: "GameEngine", level: Level) -> None:
        super().__init__()

        self.game_state = game_state
        self.player = self.createPlayer()
        self.level = level
        self.map = self.createMap()

    def input(self, key: str) -> None:
        match key:
            case "escape":
                self.game_state.displayScene(EnumScene.MENU)
            case "p":
                self.game_state.displayScene(EnumScene.PAUSE)
            case "l":
                self.game_state.displayScene(EnumScene.LOSE)
            case "v":
                self.game_state.displayScene(EnumScene.WIN)
            case "w":
                self.player.goUp()
            case "d":
                self.player.goRight()
            case "s":
                self.player.goDown()
            case "a":
                self.player.goLeft()

    def createMap(self) -> None:
        Entity(
            model="plane",
            scale=Vec3(self.level.width, 0, self.level.height),
            position=Vec3(0, 0, 0),
            color=color.black,
            collider="box",
            parent=self,
        )

        for node in self.level.levelMap.values():
            cell_x = node.pos[0] - (self.level.width / 2) + 0.5
            cell_z = -(node.pos[1] - (self.level.height / 2) + 0.5)
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

    def canMove(self, direction: int) -> bool:
        match direction:
            case 0:
                return self.player.position.z < self.level.height - 1
            case 1:
                return self.player.position.x < self.level.width - 1
            case 2:
                return self.player.position.z > 0
            case 3:
                return self.player.position.x > 0
            case _:
                return False

    def createPlayer(self) -> Player:
        return Player(parent=self)
