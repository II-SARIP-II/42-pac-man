from typing import TYPE_CHECKING

from typing_extensions import List
from ursina import Entity, Vec3, color, destroy

from src.core.Ghost import EnumMode, Ghost
from src.core.ghosts.Blinky import Blinky
from src.core.ghosts.Clyde import Clyde
from src.core.ghosts.Inky import Inky
from src.core.ghosts.Pinky import Pinky
from src.core.Level import Level
from src.core.PacGum import PacGum, SuperPacGum
from src.core.Player import Player
from src.GameData import GameData
from src.scene.LivesLayout import LivesLayout
from src.scene.Scene import Scene
from src.scene.TextLayout import TextLayout
from src.utils import convertPosToVec

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
        self.map = self.createMap()

        # Pacgums
        self.nb_pacgum = 0
        self.pacgums = self.createPacGums()
        self.current_nb_pacgum = self.nb_pacgum

        self.text_layout = TextLayout(
            self.game_engine,
            self.game_data,
        )

        self.lives_layout = LivesLayout(
            self.game_data
        )

        self.is_ghosts_moving = True

    def cleanUp(self) -> None:
        self.ignore = True
        self.disable()

        self.player.ignore = True
        for ghost in self.ghosts:
            ghost.ignore = True

        to_clean = [
            self.player,
            self.ghosts,
            self.map,
            self.pacgums,
            self.text_layout,
            self.lives_layout
        ]

        for entity in to_clean:
            if isinstance(entity, list):
                for e in entity:
                    destroy(e)
            else:
                destroy(entity)

    def input(self, key: str) -> None:
        match key:
            case "escape":
                self.game_engine.changeScene(self.game_engine.pause_scene)
            case "l":
                self.game_engine.changeScene(self.game_engine.lose_scene)
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

    def createMap(self) -> list[Entity]:
        map: list[Entity] = []
        map.append(Entity(
            model="plane",
            scale=Vec3(self.level.width, 0, self.level.height),
            position=Vec3(-0.5, 0, 0.5),
            color=color.black,
            collider="box",
            parent=self,
        ))

        for node in self.level.level_map.values():
            cell_vector = convertPosToVec(
                (node.pos), (self.level.width, self.level.height)
            )
            cell_x = cell_vector.x
            cell_z = cell_vector.z

            if not node.getNeighbour(0):
                map.append(Entity(
                    model="cube",
                    scale=Vec3(1, 2, 0.1),
                    position=Vec3(cell_x, 0.5, cell_z + 0.5),
                    color=color.blue,
                    collider="box",
                    parent=self,
                ))

            if not node.getNeighbour(1):
                map.append(Entity(
                    model="cube",
                    scale=Vec3(0.1, 2, 1),
                    position=Vec3(cell_x + 0.5, 0.5, cell_z),
                    color=color.blue,
                    collider="box",
                    parent=self,
                ))

            if not node.getNeighbour(2):
                map.append(Entity(
                    model="cube",
                    scale=Vec3(1, 2, 0.1),
                    position=Vec3(cell_x, 0.5, cell_z - 0.5),
                    color=color.blue,
                    collider="box",
                    parent=self,
                ))

            if not node.getNeighbour(3):
                map.append(Entity(
                    model="cube",
                    scale=Vec3(0.1, 2, 1),
                    position=Vec3(cell_x - 0.5, 0.5, cell_z),
                    color=color.blue,
                    collider="box",
                    parent=self,
                ))

        return map

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

    def createPacGums(self) -> list[Entity]:
        items: list[Entity] = []

        for pos, node in self.level.level_map.items():
            pos = convertPosToVec(pos, self.size)
            if node.nb_neighbours == 1:
                node.item = SuperPacGum(score=10, position=pos, parent=self)
                items.append(node.item)
                self.nb_pacgum += 1

            elif node.nb_neighbours > 1:
                node.item = PacGum(score=1, position=pos, parent=self)
                items.append(node.item)
                self.nb_pacgum += 1

        return items

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
                self.game_engine.changeScene(self.game_engine.finish_scene)
            else:
                self.game_engine.no_level += 1
                self.game_engine.changeScene(self.game_engine.win_scene)

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
            self.game_engine.changeScene(self.game_engine.lose_scene)
        self.lives_layout.displayLives()

    def onExit(self) -> None:
        self.lives_layout.disable()
        self.text_layout.disable()
        self.disable()
