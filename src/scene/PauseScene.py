from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color
from sys import exit

from src.scene.Scene import Scene
from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class PauseScene(Scene):
    """Scene shown when the player pauses an active game."""

    def __init__(self, game_state: "GameEngine"):
        """Initialize the pause scene and build its contents.

        Args:
            game_state (GameEngine): The engine managing scene
                transitions and shared game state.

        Returns:
            None.
        """
        super().__init__(game_state)

        self.game_state = game_state

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0))

        self.createScene()

        gridLayout(self.container, spacing=1.8)

    def createScene(self) -> None:
        """Build the scene's background, title, and menu buttons.

        Returns:
            None.
        """
        self.createBackground()
        self.createTitle("PAUSE")
        self.createButtons()

    def createTitle(self, title: str) -> None:
        """Create the pause scene's title text.

        Args:
            title (str): The text to display as the title.

        Returns:
            None.
        """
        self.title = TextUtils(
            text=title,
            position=Vec3(0, 1, 0),
            color=color.yellow,
            parent=self.container,
        )

    def createButtons(self) -> None:
        """Create the Resume, Instructions, Menu, and Quit buttons.

        Returns:
            None.
        """
        self.button_resume = ButtonUtils(
            text="RESUME",
            position=Vec3(0, 1, 1),
            action=lambda: self.onClickResume(),
            button_color=color.blue,
            parent=self.container,
        )

        self.button_instructions = ButtonUtils(
            text="INSTRUCTIONS",
            position=Vec3(0, 1, -5),
            action=lambda: self.onClickInstructions(),
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
        """Return to the main menu scene.

        Returns:
            None.
        """
        self.game_engine.changeScene(self.game_engine.menu_scene)

    def onClickInstructions(self) -> None:
        """Switch to the instructions scene.

        Returns:
            None.
        """
        self.game_engine.changeScene(self.game_engine.instruction_scene)

    def onClickResume(self) -> None:
        """Resume gameplay by switching back to the active game scene.

        Returns:
            None.
        """
        if self.game_engine.game_scene:
            self.game_engine.changeScene(self.game_engine.game_scene)

    def onClickQuit(self) -> None:
        """Quit the application.

        Returns:
            None.
        """
        exit()
