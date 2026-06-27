from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.UrsinaAssets.ButtonUtils import ButtonUtils

from .EnumScene import EnumScene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class WinScene(Entity):
    def __init__(self, game_state: "GameEngine"):
        super().__init__()

        self.game_state = game_state
        self.createButtons()
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

    def createButtons(self) -> None:
        self.buttonMenu()
        self.buttonQuit()

    def buttonMenu(self) -> None:
        self.button_menu = ButtonUtils(
            text="MENU",
            position=Vec3(0, 1, 1),
            action=lambda: self.game_state.displayScene(EnumScene.MENU),
            button_color=color.blue,
            parent_scene=self,
        )

    def buttonQuit(self) -> None:
        self.button_quit = ButtonUtils(
            text="Quit",
            position=Vec3(0, 1, 5),
            action=lambda: self.game_state.quitGame(),
            button_color=color.blue,
            parent_scene=self,
        )
