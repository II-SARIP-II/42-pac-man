from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.scene.Scene import Scene
from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class InstructionScene(Scene):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__(game_engine)

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0)
        )

        self.createScene()
        gridLayout(self.container, 2)

    def createScene(self) -> None:
        self.createBackground()
        self.createText()
        self.createButtons()

    def createText(self) -> None:
        self.title = TextUtils(
            parent=self.container,
            text="INSTRUCTIONS",
            color=color.yellow
        )

        TextUtils(
            parent=self.container,
            text="Movement:\nWASD or Arrows",
            scale=25.0,
            line_height=1.2
        )

        TextUtils(
            parent=self.container,
            text="Pause:\nEchap",
            scale=25.0,
            line_height=1.2
        )

        TextUtils(
            parent=self.container,
            text="Cheat mode:\nC",
            scale=25.0,
            line_height=1.2
        )

    def createButtons(self) -> None:
        self.button_return = ButtonUtils(
            text="RETURN",
            position=Vec3(0, 1, -2),
            action=lambda: self.onClickReturn(),
            button_color=color.dark_gray,
            parent=self.container,
        )

    def onClickReturn(self) -> None:
        self.game_engine.changeScene(self.game_engine.prev_scene)
