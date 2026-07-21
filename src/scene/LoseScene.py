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
    """Scene shown when the player runs out of lives."""

    def __init__(self, game_engine: "GameEngine"):
        """Initialize the lose scene and build its contents.

        Args:
            game_engine (GameEngine): The engine managing scene
                transitions and shared game state.

        Returns:
            None.
        """
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
        """Build the scene's background, title, input field, and buttons.

        Returns:
            None.
        """
        self.createBackground()
        self.createTitle()
        self.createInputField()
        self.createButtons()

    def createTitle(self) -> None:
        """Create the "Game Over" title text and score display.

        Returns:
            None.
        """
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
        """Create the Menu and Quit buttons.

        Returns:
            None.
        """
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
        """Create the name-entry input field and validate button.

        Returns:
            None.
        """
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
            action = lambda: self.submitScore()
        )

    def update(self) -> None:
        """Refresh the displayed score and the name-entry placeholder text.

        Returns:
            None.
        """
        self.score.text = f"Score: {self.game_engine.game_data.score}"

        if self.player_name.text == "":
            self.visual_name_text.text = "Enter your name..."
        else:
            self.visual_name_text.text = self.player_name.text

    def input(self, key: str) -> None:
        """Handle keyboard input for typing the player's name.

        Args:
            key (str): Key that was pressed.

        Returns:
            None.
        """
        if key == 'enter':
            self.submitScore()
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
        """Return to the main menu scene.

        Returns:
            None.
        """
        self.game_engine.changeScene(self.game_engine.menu_scene)

    def onClickQuit(self) -> None:
        """Quit the application.

        Returns:
            None.
        """
        quit()

    def onExit(self) -> None:
        """Clear the entered name and disable the scene on exit.

        Returns:
            None.
        """
        self.player_name.text=""
        self.disable()

    def submitScore(self) -> None:
        """Submit the entered name and current score to the leaderboard.

        Returns:
            None.
        """
        self.game_engine.submitScore(self.player_name.text)
