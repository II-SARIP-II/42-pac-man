from src.scene.Scene import Scene
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class HighScoreScene(Scene):
    def __init__(self, game_engine: "GameEngine", level: Level) -> None:
        super().__init__(game_engine)
