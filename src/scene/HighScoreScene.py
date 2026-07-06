from src.scene.Scene import Scene
from ursina import Entity, color, Vec3
from typing import TYPE_CHECKING
from src.models.highscore import ScoresList
from src.ursina_assets.TextUtils import TextUtils
from src.ursina_assets.utils_scene import gridLayout

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class HighScoreScene(Scene):
    def __init__(
        self,
        game_engine: "GameEngine",
        scores: ScoresList
        ) -> None:
        super().__init__(game_engine)
        self.scores = scores

        self.container = Entity(
            parent=self,
            position=Vec3(0, 0, 0))

        self.createBackground()
        self.createTitle()
        self.createHighscore()

        gridLayout(self.container, spacing=1)

    def createBackground(self) -> None:
        Entity(
            model="plane",
            scale=Vec3(20, 1, 20),
            position=Vec3(0, 0, 0),
            color=color.black,
            collider="box",
            parent=self,
        )

    def createTitle(self) -> None:
        self.title = TextUtils(
            text="-- Leaderboard --",
            parent=self.container
        )

    def createHighscore(self) -> None:
        for score in self.scores.scores:
            TextUtils(
                text=f"{score.name}: {score.score}",
                parent=self.container
            )
