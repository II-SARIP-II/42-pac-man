from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color, destroy

from src.scene.Scene import Scene
from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class LeaderboardScene(Scene):
    """Scene listing the saved high scores."""

    def __init__(
            self,
            game_engine: "GameEngine"
            ) -> None:
        """Initialize the leaderboard scene and build its contents.

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

        self.score_container = Entity(
            parent=self.container,
            position=Vec3(0, 0, 0))

        self.createScene()

    def createScene(self) -> None:
        """Build the scene's background, title, and menu button.

        Returns:
            None.
        """
        self.createBackground()
        self.createTitle()
        self.createButtons()

    def createTitle(self) -> None:
        """Create the leaderboard title text.

        Returns:
            None.
        """
        self.title = TextUtils(
            text="LEADERBOARD",
            parent=self.container,
            color=color.yellow,
            position=Vec3(0, 1, 5)
        )

    def createHighscore(self) -> None:
        """Rebuild the list of displayed high scores.

        Returns:
            None.
        """
        for child in self.score_container.children:
            destroy(child)

        self.score_container.children = []

        for score in self.game_engine.highscores.scores:
            TextUtils(
                text=f"{score.name}: {score.score}",
                parent=self.score_container,
                scale=25.0,
            )

    def createButtons(self) -> None:
        """Create the button that returns to the main menu.

        Returns:
            None.
        """
        self.button_menu = ButtonUtils(
            text="MENU",
            action=lambda: self.onClickMenu(),
            button_color=color.dark_gray,
            parent=self.container,
            position=Vec3(0, 0.1, -6.5)
        )

    def onEntry(self) -> None:
        """Enable the scene and refresh the displayed high scores.

        Returns:
            None.
        """
        self.enable()
        self.createHighscore()

        gridLayout(self.score_container, spacing=0.8)

    def onClickMenu(self) -> None:
        """Return to the main menu scene.

        Returns:
            None.
        """
        self.game_engine.changeScene(self.game_engine.menu_scene)
