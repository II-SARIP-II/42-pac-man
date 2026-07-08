from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color, destroy

from src.scene.Scene import Scene
from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class LeaderboardScene(Scene):
    def __init__(
            self,
            game_engine: "GameEngine"
            ) -> None:

        super().__init__(game_engine)

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0))

        self.score_container = Entity(
            parent=self.container,
            position=Vec3(0, 0, 0))

        self.createScene()

    def createScene(self) -> None:
        self.createBackground()
        self.createTitle()
        self.createButtons()

    def createTitle(self) -> None:
        self.title = TextUtils(
            text="LEADERBOARD",
            parent=self.container,
            color=color.yellow,
            position=Vec3(0, 1, 5)
        )

    def createHighscore(self) -> None:
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
        self.button_menu = ButtonUtils(
            text="MENU",
            action=lambda: self.onClickMenu(),
            button_color=color.dark_gray,
            parent=self.container,
            position=Vec3(0, 0.1, -6.5)
        )

    def onEntry(self) -> None:
        self.enable()
        self.createHighscore()

        gridLayout(self.score_container, spacing=0.8)

    def onClickMenu(self) -> None:
        self.game_engine.changeScene(self.game_engine.menu_scene)
