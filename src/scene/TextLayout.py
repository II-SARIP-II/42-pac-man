from ursina import color, Vec2, Entity, camera, Text
import ursina
from typing import TYPE_CHECKING, Any
from src.GameData import GameData

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class TextLayout(Entity):
    def __init__(self,
                 game_engine: "GameEngine",
                 game_data: GameData,
                 multiplier: float = 1,
                 **kwargs: Any
                 ) -> None:
        if multiplier < 0:
            raise ValueError("Multiplier must be positive")

        super().__init__(
            parent=camera.ui,
            position=Vec2(-0.85, 0.45),
            origin=Vec2(-0.5, 0.5),
            **kwargs
        )
        self.game_data = game_data
        self.game_engine = game_engine

        self.text_entity = Text(
            text="",
            position=Vec2(0, 0),
            color=color.white,
            parent=self,
            scale=1.5
        )
        self.refresh_text()

    def refresh_text(self) -> None:
        txt = (f"Score: {self.game_data.score}\n"
               f"Death: {self.game_data.nb_death}\n"
               f"Time: {max(0, int(self.game_data.game_time))}\n")

        if self.text_entity:
            self.text_entity.text = txt

    def update(self) -> None:
        from src.scene.EnumScene import EnumScene
        if self.game_engine.state == EnumScene.GAME:
            self.game_data.removeTime(ursina.time.dt)
            self.refresh_text()
