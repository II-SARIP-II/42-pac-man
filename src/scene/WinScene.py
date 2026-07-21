from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

from .Scene import Scene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class WinScene(Scene):
    """Scene shown when the player finishes a non-final level."""

    def __init__(self, game_engine: "GameEngine"):
        """Initialize the win scene and build its contents.

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

        gridLayout(self.container_texts, 1)
        gridLayout(self.container_buttons, 1.8)
        gridLayout(self.container, 4)

    def createScene(self) -> None:
        """Build the scene's background, title, and buttons.

        Returns:
            None.
        """
        self.createBackground()
        self.createTitle("YOU WIN!")
        self.createButtons()

    def createTitle(self, title: str) -> None:
        """Create the win scene's title text and score display.

        Args:
            title (str): The text to display as the title.

        Returns:
            None.
        """
        self.title = TextUtils(
            parent=self.container_texts,
            text=title,
            color=color.yellow
        )

        self.score = TextUtils(
            parent=self.container_texts,
            text=f"Score: {self.game_engine.game_data.score}"
        )

    def createButtons(self) -> None:
        """Create the Next Level, Menu, and Quit buttons.

        Returns:
            None.
        """
        self.button_next_level = ButtonUtils(
            text="NEXT LEVEL",
            action=lambda: self.onClickNextLevel(),
            button_color=color.blue,
            parent=self.container_buttons,
        )

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

    def update(self) -> None:
        """Refresh the displayed score.

        Returns:
            None.
        """
        self.score.text = f"Score: {self.game_engine.game_data.score}"

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

    def onClickNextLevel(self) -> None:
        """Advance to the next level.

        Returns:
            None.
        """
        self.game_engine.nextLevel()
