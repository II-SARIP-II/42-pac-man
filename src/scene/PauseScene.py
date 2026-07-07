from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

from .EnumScene import EnumScene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class PauseScene(Entity):
    def __init__(self, game_state: "GameEngine"):
        super().__init__()

        self.game_state = game_state
        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0)
        )

        self.createBackground()
        self.createTitle()
        self.createButtons()

        gridLayout(self.container, spacing=1.8)

    def createBackground(self) -> None:
        Entity(
            model="plane",
            scale=Vec3(20, 1, 20),
            position=Vec3(0, 0, 0),
            color=color.black,
            collider="box",
            parent=self,
        )

    def createTitle(self) -> None:
        TextUtils(
            text="PAUSE",
            position=Vec3(0, 1, 0),
            color=color.white,
            parent=self.container,
        )

    def createButtons(self) -> None:
        self.button_resume = ButtonUtils(
            text="RESUME",
            position=Vec3(0, 1, 1),
            action=lambda: self.game_state.displayScene(EnumScene.RESUME),
            button_color=color.blue,
            parent=self.container,
        )

        self.button_menu = ButtonUtils(
            text="MENU",
            position=Vec3(0, 1, -2),
            action=lambda: self.game_state.displayScene(EnumScene.MENU),
            button_color=color.red,
            parent=self.container,
        )

        self.button_quit = ButtonUtils(
            text="QUIT",
            position=Vec3(0, 1, -5),
            action=lambda: self.game_state.quitGame(),
            button_color=color.dark_gray,
            parent=self.container,
        )
