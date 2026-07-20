from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color
from ursina.prefabs.input_field import InputField

from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

from .Scene import Scene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class LoseScene(Scene):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__(game_engine)

        self.container = Entity(
            parent=self, position=Vec3(0, 0, 0))
        self.container_texts = Entity(
            parent=self.container, position=Vec3(0, 0, 0))
        self.container_buttons = Entity(
            parent=self.container, position=Vec3(0, 0, 0))

        self.createScene()

        gridLayout(self.container_texts, 1.2)
        gridLayout(self.container_buttons, 1.8)
        gridLayout(self.container, 5)

    def createScene(self) -> None:
        self.createBackground()
        self.createTitle()
        self.createInputField()
        self.createButtons()

    def createTitle(self) -> None:
        self.title = TextUtils(
            parent=self.container_texts,
            text="Game Over",
            color=color.yellow
        )

        self.score = TextUtils(
            parent=self.container_texts,
            text=f"Score: {self.game_engine.game_data.score}"
        )

    def createButtons(self) -> None:
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

    def createInputField(self) -> None:
        self.player_name = InputField(
            enabled=False
        )

        self.visual_name_text = TextUtils(
            parent=self.container_texts,
            text="Enter your name...",
        )

        self.validate_button = ButtonUtils(
            text="VALIDATE",
            parent=self.container_buttons,
            action=lambda: self.game_engine.submitScore(
                self.player_name.text),
        )

    def update(self) -> None:
        self.score.text = f"Score: {self.game_engine.game_data.score}"

        if self.player_name.text == "":
            self.visual_name_text.text = "Enter your name..."
        else:
            self.visual_name_text.text = self.player_name.text

    def input(self, key: str) -> None:
        if key == 'enter':
            self.game_engine.submitScore(self.player_name.text)
            return

        if key == 'backspace':
            if len(self.player_name.text) > 0:
                self.player_name.text = self.player_name.text[:-1]
            return

        if key == 'space':
            self.player_name.text += ' '
            return

        if len(key) == 1 and len(self.player_name.text) < 10:
            if key.isalnum():
                self.player_name.text += key

    def onClickMenu(self) -> None:
        self.game_engine.changeScene(self.game_engine.menu_scene)

    def onClickQuit(self) -> None:
        quit()

    def onExit(self) -> None:
        self.player_name.text=""
        self.disable()
