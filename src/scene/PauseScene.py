from typing import TYPE_CHECKING

from ursina import Entity, Vec2, Vec3, color

from src.UrsinaAssets.ButtonUtils import ButtonUtils
from src.UrsinaAssets.TextUtils import TextUtils

from .EnumScene import EnumScene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class PauseScene(Entity):
    def __init__(self, game_state: "GameEngine"):
        super().__init__()

        self.game_state = game_state
        self.createButtons()
        self.createTitleText()
        self.createBackground()

    def createBackground(self) -> None:
        Entity(
            model="plane",
            scale=Vec3(20, 1, 20),
            position=Vec3(0, 0, 0),
            color=color.black,
            collider="box",
            parent=self,
        )

    def createTitleText(self) -> None:
        TextUtils(
            text="PAUSE",
            position=Vec3(0, 1, 0),
            color=color.white,
            parent=self,
            origin=Vec2(0, -5),
        )

    def createButtons(self) -> None:
        self.button_resume = ButtonUtils(
            text="RESUME",
            position=Vec3(0, 1, 1),
            action=lambda: self.game_state.displayScene(EnumScene.GAME),
            button_color=color.blue,
            parent_scene=self,
        )

        self.button_menu = ButtonUtils(
            text="MAIN MENU",
            position=Vec3(0, 1, -2),
            action=lambda: self.game_state.displayScene(EnumScene.MENU),
            button_color=color.red,
            parent_scene=self,
        )

        self.button_quit = ButtonUtils(
            text="QUIT",
            position=Vec3(0, 1, -5),
            action=lambda: self.game_state.quitGame(),
            button_color=color.dark_gray,
            parent_scene=self,
        )
