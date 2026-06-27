from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.UrsinaAssets.ButtonUtils import ButtonUtils

from .EnumScene import EnumScene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class MenuScene(Entity):
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
        self.buttonPlay()
        self.buttonQuit()

    def buttonPlay(self) -> None:
        self.button_game = ButtonUtils(
            text="Play",
            position=Vec3(0, 1, 1),
            parent_scene=self,
            button_color=color.blue,
            action=lambda: self.game_state.displayScene(EnumScene.GAME),
        )

    def buttonQuit(self) -> None:
        self.button_quit = ButtonUtils(
            text="Quit",
            position=Vec3(0, 1, -2),
            action=lambda: self.game_state.quitGame(),
            button_color=color.blue,
            parent_scene=self,
        )
