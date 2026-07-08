from faulthandler import enable
from typing import TYPE_CHECKING

from ursina import Entity, Vec3, camera, color
from ursina.prefabs.input_field import InputField

from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

from .Scene import Scene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class FinishScene(Scene):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__(game_engine)

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0))

        self.createScene()

        gridLayout(self.container, 1.8)

    def createScene(self) -> None:
        self.createBackground()
        self.createTitle()
        self.createInputField()
        self.createButtons()

    def createInputField(self) -> None:
        self.player_name = InputField(
            enabled=False
        )

        self.visual_name_text = TextUtils(
            parent=self.container,
            text="Enter your name..."
        )

        self.validate_button = ButtonUtils(
            text="Validate",
            parent=self.container,
            action=lambda: self.game_engine.submitScore(),
        )

    def createButtons(self) -> None:
        self.button_game = ButtonUtils(
            text="Menu",
            position=Vec3(0, 1, 1),
            parent=self.container,
            button_color=color.blue,
            action=lambda: self.onClickMenu(),
        )

        self.button_quit = ButtonUtils(
            text="Quit",
            position=Vec3(0, 1, -2),
            action=lambda: self.onClickQuit(),
            button_color=color.blue,
            parent=self.container,
        )

    def createTitle(self) -> None:
        self.title = TextUtils(
            parent=self.container,
            text="You finished the game\ncongrats!",
            color=color.yellow,
            scale=40
        )

        self.score = TextUtils(
            parent=self.container,
            text=f"Score: {self.game_engine.game_data.score}",
        )

    def update(self) -> None:
        self.score.text = f"Score: {self.game_engine.game_data.score}"

        if self.player_name.text == "":
            self.visual_name_text.text = "Enter your name..."
        else:
            self.visual_name_text.text = self.player_name.text

    def input(self, key: str) -> None:
        if key == 'enter':
            self.game_engine.submitScore()
            return

        if key == 'backspace':
            if len(self.player_name.text) > 0:
                self.player_name.text = self.player_name.text[:-1]
            return

        if key == 'space':
            self.player_name.text += ' '
            return

        if len(key) == 1 and len(self.player_name.text) < 12:
            self.player_name.text += key

    def onExit(self) -> None:
        self.player_name.text = ""
        self.disable()

    def onClickQuit(self) -> None:
        quit()

    def onClickMenu(self) -> None:
        self.game_engine.changeScene(self.game_engine.menu_scene)
