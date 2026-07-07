from ursina import Entity
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class Scene(Entity):
    def __init__(self, game_engine: "GameEngine"):
        super().__init__()

        self.game_engine = game_engine

    def on_enter(self) -> None:
        pass

    def on_exit(self) -> None:
        pass
