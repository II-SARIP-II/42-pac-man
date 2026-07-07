from typing import TYPE_CHECKING

from typing_extensions import List
from ursina import Entity, Vec3, color
from src.scene.TextLayout import TextLayout
from src.scene.LivesLayout import LivesLayout
from src.core.Ghost import Ghost
from src.core.ghosts.Blinky import Blinky
from src.core.ghosts.Clyde import Clyde
from src.core.ghosts.Inky import Inky
from src.core.ghosts.Pinky import Pinky
from src.core.Level import Level
from src.core.PacGum import PacGum, SuperPacGum
from src.core.Player import Player
from src.scene.EnumScene import EnumScene
from src.scene.Scene import Scene
from src.utils import convertPosToVec
from src.core.Ghost import EnumMode
from src.GameData import GameData

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class GameScene(Scene):
    def __init__(
            self,
            game_engine: "GameEngine",
            game_data: GameData,
            level: Level
            ) -> None:
        super().__init__(game_engine)

        self.game_engine = game_engine
        self.game_data = game_data
        self.level = level
        self.size = self.level.width, self.level.height
        self.player = self.createPlayer(
            self.level.width,
            self.level.height,
            game_data
            )
        self.ghosts: List[Ghost] = self.createGhosts(
            self.level.width, self.level.height, self.player, self.level
        )
        self.nb_pacgum = 0
        self.createMap()
        self.createPacGums()
        self.current_nb_pacgum = self.nb_pacgum

        self.text_layout = TextLayout(
            self.game_engine,
            self.game_data,
        )

        self.lives_layout = LivesLayout(
            self.game_data
        )

        self.is_ghosts_moving = True

    def input(self, key: str) -> None:
        match key:
            case "escape":
                self.game_engine.displayScene(EnumScene.PAUSE)
            case "l":
                self.game_engine.displayScene(EnumScene.LOSE)
            case "v":
                self.current_nb_pacgum = 0
            case "w" | "up arrow":
                self.player.wish_direction = 0
            case "d" | "right arrow":
                self.player.wish_direction = 1
            case "s" | "down arrow":
                self.player.wish_direction = 2
            case "a" | "left arrow":
                self.player.wish_direction = 3
            case "m":
                self.toggleMovingGhosts()
            case "x":
                self.toggleInfiniteLives()
            case "c":
                self.toggleAllCheat()

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
            cell_vector = convertPosToVec(
                (node.pos), (self.level.width, self.level.height)
            )
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

    def createPlayer(
            self,
            width: int,
            height: int,
            game_data: GameData
            ) -> Player:
        return Player(
            parent=self,
            width=width,
            height=height,
            game_data=game_data)

    def createPacGums(self) -> None:
        for pos, node in self.level.level_map.items():
            pos = convertPosToVec(pos, self.size)
            if node.nb_neighbours == 1:
                node.item = SuperPacGum(score=10, position=pos, parent=self)
                self.nb_pacgum += 1

            elif node.nb_neighbours > 1:
                node.item = PacGum(score=1, position=pos, parent=self)
                self.nb_pacgum += 1

    def createGhosts(
        self, width: int, height: int, player: Player, level: Level
    ) -> List[Ghost]:
        return [
            Blinky(
                parent=self,
                width=width,
                height=height,
                player=player,
                level=level
                ),
            Pinky(
                parent=self,
                width=width,
                height=height,
                player=player,
                level=level
                ),
            Inky(
                parent=self,
                width=width,
                height=height,
                player=player,
                level=level
                ),
            Clyde(
                parent=self,
                width=width,
                height=height,
                player=player,
                level=level
                )
        ]

    def isTheLevelFinished(self) -> None:
        if self.current_nb_pacgum <= 0:
            if self.game_engine.no_level == self.game_engine.nb_level:
                self.game_engine.displayScene(EnumScene.FINISH)
            else:
                self.game_engine.no_level += 1
                self.game_engine.displayScene(EnumScene.WIN)

    def toggleAllCheat(self) -> None:
        self.toggleMovingGhosts()
        self.toggleInfiniteLives()

    def toggleMovingGhosts(self) -> None:
        self.is_ghosts_moving = not self.is_ghosts_moving
        if not self.is_ghosts_moving:
            for ghost in self.ghosts:
                ghost.mode = EnumMode.STOP
        else:
            for ghost in self.ghosts:
                ghost.mode = EnumMode.CHASE

    def toggleInfiniteLives(self) -> None:
        self.game_data.infiniteLives()
        self.lives_layout.infiniteLive()

    def killPlayer(self) -> None:
        self.player.loseLife()
        self.game_data.playerDead()
        if self.game_data.lives <= 0:
            self.game_engine.displayScene(EnumScene.LOSE)
        self.lives_layout.displayLives()
