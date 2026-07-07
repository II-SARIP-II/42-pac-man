from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

from .Scene import Scene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class MenuScene(Scene):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__(game_engine)

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0))

        self.createScene()

        gridLayout(self.container, 1.8)

    def createScene(self) -> None:
        self.createBackground()
        self.createTitle("PACMAN")
        self.createButtons()

    def createButtons(self) -> None:
        self.button_play = ButtonUtils(
            text="PLAY",
            position=Vec3(0, 1, 1),
            parent=self.container,
            button_color=color.blue,
            action=lambda: self.onClickPlay(),
        )

        self.button_leaderboard = ButtonUtils(
            text="LEADERBOARD",
            position=Vec3(0, 1, -2),
            action=lambda: self.onClickLeaderboard(),
            button_color=color.blue,
            parent=self.container,
        )

        self.button_quit = ButtonUtils(
            text="QUIT",
            position=Vec3(0, 1, -2),
            action=lambda: self.onClickQuit(),
            button_color=color.blue,
            parent=self.container,
        )

    def createTitle(self, title: str) -> None:
        self.title = TextUtils(
            parent=self.container,
            text=title
        )

    def onClickPlay(self) -> None:
        self.game_engine.resetGameData()
        self.game_engine.newGameScene()
        self.game_engine.changeScene(self.game_engine.game_scene)

    def onClickLeaderboard(self) -> None:
        self.game_engine.changeScene(self.game_engine.leaderboard_scene)

    def onClickQuit(self) -> None:
        quit()
