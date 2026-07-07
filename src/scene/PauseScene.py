from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.scene.Scene import Scene
from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class PauseScene(Scene):
    def __init__(self, game_state: "GameEngine"):
        super().__init__(game_state)

        self.game_state = game_state

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0))

        self.createScene()

        gridLayout(self.container, spacing=1.8)

    def createScene(self) -> None:
        self.createBackground()
        self.createTitle("PAUSE")
        self.createButtons()

    def createTitle(self, title: str) -> None:
        self.title = TextUtils(
            text=title,
            position=Vec3(0, 1, 0),
            color=color.white,
            parent=self.container,
        )

    def createButtons(self) -> None:
        self.button_resume = ButtonUtils(
            text="RESUME",
            position=Vec3(0, 1, 1),
            action=lambda: self.onClickResume(),
            button_color=color.blue,
            parent=self.container,
        )

        self.button_menu = ButtonUtils(
            text="MENU",
            position=Vec3(0, 1, -2),
            action=lambda: self.onClickMenu(),
            button_color=color.dark_gray,
            parent=self.container,
        )

        self.button_quit = ButtonUtils(
            text="QUIT",
            position=Vec3(0, 1, -5),
            action=lambda: self.onClickQuit(),
            button_color=color.red,
            parent=self.container,
        )

    def onClickMenu(self) -> None:
        self.game_engine.changeScene(self.game_engine.menu_scene)

    def onClickQuit(self) -> None:
        quit()

    def onClickResume(self) -> None:
        self.game_engine.changeScene(self.game_engine.game_scene)
