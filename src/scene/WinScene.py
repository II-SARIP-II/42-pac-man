from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

from .Scene import Scene
from src.GameData import GameData

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class WinScene(Scene):
    def __init__(self, game_engine: "GameEngine", game_data: GameData):
        super().__init__(game_engine)

        self.game_data = game_data

        self.container = Entity(
            parent=self, position=Vec3(0, 0, 0))
        self.container_texts = Entity(
            parent=self.container, position=Vec3(0, 0, 0))
        self.container_buttons = Entity(
            parent=self.container, position=Vec3(0, 0, 0))

        self.createScene()

        gridLayout(self.container_texts, 1)
        gridLayout(self.container_buttons, 1.8)
        gridLayout(self.container, 4)

    def createScene(self) -> None:
        self.createBackground()
        self.createTitle("YOU WIN!")
        self.createButtons()

    def createTitle(self, title: str) -> None:
        self.title = TextUtils(
            parent=self.container_texts,
            text=title,
        )

        self.score = TextUtils(
            parent=self.container_texts,
            text=f"Score: {self.game_data.score}"
        )

    def createButtons(self) -> None:
        self.button_next_level = ButtonUtils(
            text="NEXT LEVEL",
            action=lambda: self.onClickNextLevel(),
            button_color=color.blue,
            parent=self.container_buttons,
        )

        self.button_menu = ButtonUtils(
            text="MENU",
            action=lambda: self.onClickMenu(),
            button_color=color.blue,
            parent=self.container_buttons,
        )

        self.button_quit = ButtonUtils(
            text="QUIT",
            action=lambda: self.onClickQuit(),
            button_color=color.blue,
            parent=self.container_buttons,
        )

    def onClickMenu(self) -> None:
        self.game_engine.changeScene(self.game_engine.menu_scene)

    def onClickQuit(self) -> None:
        quit()

    def onClickNextLevel(self) -> None:
        self.game_engine.nextLevel()
