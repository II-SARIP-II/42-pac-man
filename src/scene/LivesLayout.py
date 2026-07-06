from ursina import color, Vec2, Entity, camera, destroy
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class LivesLayout(Entity):
    def __init__(self,
                 game_engine: "GameEngine",
                 lives: int = 3,
                 **kwargs
                 ):
        super().__init__(
            parent=camera.ui,
            position=Vec2(-0.85, -0.45),
            origin=Vec2(-0.5, -0.5),
            **kwargs
        )
        self.lives = lives
        self.engine = game_engine
        self.infinite = False
        self.life_entities = []
        self.displayLives()

    def displayLives(self):
        if not self.infinite:
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
        else:
            life_icon = Entity(
                    model="quad",
                    scale=(0.1, 0.1),
                    position=Vec2(0.06, 0),
                    texture="assets/images/infinity_yellow.png",
                    parent=self,
                    color=color.yellow
                )
            self.life_entities.append(life_icon)

    def infiniteLive(self):
        for i in range(len(self.life_entities)):
            last_icon = self.life_entities.pop()
            destroy(last_icon)
        self.infinite = not self.infinite
        self.displayLives()

    def loseLife(self):
        if self.lives > 0 and self.life_entities:
            self.lives -= 1
            last_icon = self.life_entities.pop()
            destroy(last_icon)
