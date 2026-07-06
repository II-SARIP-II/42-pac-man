from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

from .EnumScene import EnumScene
from .Scene import Scene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class WinScene(Scene):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__(game_engine)

        self.container = Entity(
            parent=self, position=Vec3(0, 0, 0))

        self.container_texts = Entity(
            parent=self.container, position=Vec3(0, 0, 0))

        self.container_buttons = Entity(
            parent=self.container, position=Vec3(0, 0, 0))

        self.createBackground()
        self.createTitle()
        self.createButtons()

        gridLayout(self.container_texts, 1)
        gridLayout(self.container_buttons, 1.8)
        gridLayout(self.container, 4)

    def createBackground(self) -> None:
        Entity(
            model="plane",
            scale=Vec3(20, 0, 20),
            position=Vec3(0, 0, 0),
            color=color.black,
            collider="box",
            parent=self,
        )

    def createTitle(self) -> None:
        self.title = TextUtils(
            parent=self.container_texts,
            text="You win!",
        )

        self.score = TextUtils(
            parent=self.container_texts,
            text=f"Score: {self.game_engine.current_score}"
        )

    def createButtons(self) -> None:
        self.button_menu = ButtonUtils(
            text="MENU",
            action=lambda: self.game_engine.displayScene(EnumScene.MENU),
            button_color=color.blue,
            parent=self.container_buttons,
        )

        self.button_quit = ButtonUtils(
            text="QUIT",
            action=lambda: self.game_engine.quitGame(),
            button_color=color.blue,
            parent=self.container_buttons,
        )

        self.button_next_level = ButtonUtils(
            text="NEXT LEVEL",
            action=lambda: self.game_engine.nextLevel(),
            button_color=color.blue,
            parent=self.container_buttons,
        )
