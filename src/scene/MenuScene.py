from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

from .EnumScene import EnumScene
from .Scene import Scene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class MenuScene(Scene):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__(game_engine)

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0))

        self.createBackground()
        self.createTitle()
        self.createButtons()

        gridLayout(self.container, 1.8)

    def createBackground(self) -> None:
        Entity(
            model="plane",
            scale=Vec3(20, 1, 20),
            position=Vec3(0, 0, 0),
            color=color.black,
            collider="box",
            parent=self,
        )

    def createButtons(self) -> None:
        self.button_game = ButtonUtils(
            text="PLAY",
            position=Vec3(0, 1, 1),
            parent=self.container,
            button_color=color.blue,
            action=lambda: self.game_engine.displayScene(EnumScene.GAME),
        )

        self.button_quit = ButtonUtils(
            text="LEADERBOARD",
            position=Vec3(0, 1, -2),
            action=lambda: self.game_engine.displayScene(EnumScene.HIGHSCORE),
            button_color=color.blue,
            parent=self.container,
        )

        self.button_quit = ButtonUtils(
            text="QUIT",
            position=Vec3(0, 1, -2),
            action=lambda: self.game_engine.quitGame(),
            button_color=color.blue,
            parent=self.container,
        )

    def createTitle(self) -> None:
        self.titel = TextUtils(
            parent=self.container,
            text="PACMAN"
        )

    def on_enter(self) -> None:
        self.game_engine.resetGame()
