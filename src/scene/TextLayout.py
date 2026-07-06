from ursina import color, Vec2, Entity, camera, Text
import ursina
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class TextLayout(Entity):
    def __init__(self,
                 game_engine: "GameEngine",
                 time: int = 90,
                 multiplier: float = 1,
                 **kwargs
                 ):
        if multiplier < 0:
            raise ValueError("Multiplier must be positive")

        super().__init__(
            parent=camera.ui,
            position=Vec2(-0.85, 0.45),
            origin=Vec2(-0.5, 0.5),
            **kwargs
        )
        self.score = 0
        self.death = 0
        self.time = time
        self.game_engine = game_engine

        self.text_entity = Text(
            text="",
            position=Vec2(0, 0),
            color=color.white,
            parent=self,
            scale=1.5
        )
        self.refresh_text()

    def add_death(self):
        self.death += 1

    def refresh_text(self):
        txt = (f"Score: {self.game_engine.current_score}\n"
               f"Death: {self.death}\n"
               f"Time: {max(0, int(self.time))}\n")

        if self.text_entity:
            self.text_entity.text = txt

    def update(self):
        from src.scene.EnumScene import EnumScene
        if self.game_engine.state == EnumScene.GAME:
            self.time -= ursina.time.dt
            self.refresh_text()
