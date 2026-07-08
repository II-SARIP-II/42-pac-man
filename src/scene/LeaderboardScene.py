from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.models.highscore import ScoresList
from src.scene.Scene import Scene
from src.ursina_assets.ButtonUtils import ButtonUtils
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class LeaderboardScene(Scene):
    def __init__(
            self,
            game_engine: "GameEngine",
            scores: ScoresList
            ) -> None:

        super().__init__(game_engine)

        self.scores_list = scores

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0))

        self.text_container = Entity(
            parent=self.container,
            position=Vec3(0, 0, 3))

        self.createScene()

        gridLayout(self.text_container, spacing=1)

    def createScene(self) -> None:
        self.createBackground()
        self.createTitle()
        self.createHighscore()
        self.createButtons()

    def createTitle(self) -> None:
        self.title = TextUtils(
            text="LEADERBOARD",
            parent=self.container,
            color=color.yellow,
            position=Vec3(0, 1, 6)
        )

    def createHighscore(self) -> None:
        for score in self.scores_list.scores:
            TextUtils(
                text=f"{score.name}: {score.score}",
                parent=self.text_container,
                scale=25.0,
                origin=(0, 0.5)
            )

    def createButtons(self) -> None:
        self.button_menu = ButtonUtils(
            text="MENU",
            action=lambda: self.onClickMenu(),
            button_color=color.dark_gray,
            parent=self.container,
            position=Vec3(0, 0.1, -6.5)
        )

    def onClickMenu(self) -> None:
        self.game_engine.changeScene(self.game_engine.menu_scene)
