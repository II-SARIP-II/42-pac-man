from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.core.Level import Level
from src.core.Player import Player
from src.scene.EnumScene import EnumScene
from src.utils import convertPosToVec

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class GameScene(Entity):
    def __init__(self, game_engine: "GameEngine", level: Level) -> None:
        super().__init__()

        self.game_engine = game_engine
        self.level = level
        self.player = self.createPlayer(self.level.width, self.level.height)
        self.map = self.createMap()

    def input(self, key: str) -> None:
        match key:
            case "escape":
                self.game_engine.displayScene(EnumScene.MENU)
            case "p":
                self.game_engine.displayScene(EnumScene.PAUSE)
            case "l":
                self.game_engine.displayScene(EnumScene.LOSE)
            case "v":
                self.game_engine.displayScene(EnumScene.WIN)
            case "w":
                self.player.wish_direction = 0
            case "d":
                self.player.wish_direction = 1
            case "s":
                self.player.wish_direction = 2
            case "a":
                self.player.wish_direction = 3

    def createMap(self) -> None:
        Entity(
            model="plane",
            scale=Vec3(self.level.width, 0, self.level.height),
            position=Vec3(-0.5, 0, 0.5),
            color=color.black,
            collider="box",
            parent=self,
        )

        for node in self.level.level_map.values():
            cell_vector = convertPosToVec((node.pos), (self.level.width, self.level.height))
            cell_x = cell_vector.x
            cell_z = cell_vector.z

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

    def createPlayer(self, width: int, height: int) -> Player:
        return Player(parent=self, width=width, height=height)
