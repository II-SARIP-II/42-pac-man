from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color
from sys import exit

from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

from .Scene import Scene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class MenuScene(Scene):
    """The main menu scene, the entry point of the game."""

    def __init__(self, game_engine: "GameEngine"):
        """Initialize the menu scene and build its contents.

        Args:
            game_engine (GameEngine): The engine managing scene
                transitions and shared game state.

        Returns:
            None.
        """
        super().__init__(game_engine)

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0))

        self.createScene()

        gridLayout(self.container, 1.8)

    def createScene(self) -> None:
        """Build the scene's background, title, and menu buttons.

        Returns:
            None.
        """
        self.createBackground()
        self.createTitle("PACMAN")
        self.createButtons()

    def createButtons(self) -> None:
        """Create the Play, Leaderboard, Instructions, and Quit buttons.

        Returns:
            None.
        """
        self.button_play = ButtonUtils(
            text="PLAY",
            position=Vec3(0, 1, 1),
            parent=self.container,
            button_color=color.blue,
            action=lambda: self.onClickPlay(),
        )

        self.button_leaderboard = ButtonUtils(
            text="LEADERBOARD",
            position=Vec3(0, 1, -2),
            action=lambda: self.onClickLeaderboard(),
            button_color=color.blue,
            parent=self.container,
        )

        self.button_instruction = ButtonUtils(
            text="INSTRUCTIONS",
            position=Vec3(0, 1, -2),
            action=lambda: self.onClickInstruction(),
            button_color=color.blue,
            parent=self.container,
        )

        self.button_quit = ButtonUtils(
            text="QUIT",
            position=Vec3(0, 1, -2),
            action=lambda: self.onClickQuit(),
            button_color=color.blue,
            parent=self.container,
        )

    def createTitle(self, title: str) -> None:
        """Create the menu's title text.

        Args:
            title (str): The text to display as the menu title.

        Returns:
            None.
        """
        self.title = TextUtils(
            parent=self.container,
            text=title
        )

    def onClickPlay(self) -> None:
        """Start a new game and switch to the game scene.

        Returns:
            None.
        """
        self.game_engine.resetGameData()
        self.game_engine.level_generator.seeded = False
        self.game_engine.initLevel()
        self.game_engine.newGameScene()

        if self.game_engine.game_scene:
            self.game_engine.changeScene(self.game_engine.game_scene)

    def onClickLeaderboard(self) -> None:
        """Switch to the leaderboard scene.

        Returns:
            None.
        """
        self.game_engine.changeScene(self.game_engine.leaderboard_scene)

    def onClickQuit(self) -> None:
        """Quit the application.

        Returns:
            None.
        """
        exit()

    def onClickInstruction(self) -> None:
        """Switch to the instructions scene.

        Returns:
            None.
        """
        self.game_engine.changeScene(self.game_engine.instruction_scene)
