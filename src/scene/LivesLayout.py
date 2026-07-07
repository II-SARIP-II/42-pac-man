from ursina import color, Vec2, Entity, camera, destroy, Text
from typing import TYPE_CHECKING, Any
from src.GameEngine import EnumScene

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class LivesLayout(Entity):
    def __init__(self,
                 game_engine: "GameEngine",
                 lives: int = 3,
                 **kwargs: Any
                 ):
        super().__init__(
            parent=camera.ui,
            position=Vec2(-0.85, -0.45),
            origin=Vec2(-0.5, -0.5),
            **kwargs
        )
        self.lives = lives
        self.game_engine = game_engine
        self.infinite = False
        self.life_entities: list[Entity] = []

        self.text_entity = Text(
            text="",
            position=Vec2(0.12, 0),
            color=color.white,
            parent=self,
            scale=1.5
        )

        self.displayLives()

    def clear_icons(self) -> None:
        """Supprime proprement toutes les entités d'icônes actuelles."""
        for icon in self.life_entities:
            destroy(icon)
        self.life_entities.clear()

    def displayLives(self) -> None:
        self.clear_icons()

        if self.infinite:
            self.text_entity.text = ""
            life_icon = Entity(
                model="quad",
                scale=(0.1, 0.1),
                position=Vec2(0.06, 0),
                texture="assets/images/infinity_yellow.png",
                parent=self,
                color=color.yellow
            )
            self.life_entities.append(life_icon)
            return

        if self.lives > 9:
            life_icon = Entity(
                model="quad",
                scale=(0.05, 0.05),
                position=Vec2(0.06, 0),
                texture="assets/images/pacman.png",
                parent=self,
                color=color.yellow,
            )
            self.life_entities.append(life_icon)
            self.text_entity.text = f"x{self.lives}"

        else:
            self.text_entity.text = ""
            for i in range(self.lives):
                life_icon = Entity(
                    model="quad",
                    scale=(0.05, 0.05),
                    position=Vec2(i * 0.06, 0),
                    texture="assets/images/pacman.png",
                    parent=self,
                    color=color.yellow,
                )
                self.life_entities.append(life_icon)

    def infiniteLive(self) -> None:
        self.infinite = not self.infinite
        self.displayLives()

    def loseLife(self) -> None:
        if self.lives > 0:
            self.lives -= 1
            self.displayLives()

        if self.lives <= 0:
            self.game_engine.displayScene(EnumScene.LOSE)
