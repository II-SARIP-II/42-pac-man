from src.UrsinaAssets.TextUtils import TextUtils
from ursina import Vec3, color, Vec2, Entity, camera
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class Layout(Entity):
    def __init__(self,
                 game_engine: "GameEngine",
                 lives: int = 3,
                 time: int = 90,
                 pacgum_score: int = 5,
                 super_pacgum_score: int = 20,
                 ghost_score: int = 100,
                 malus_death: int = 0,
                 multiplier: float = 1,
                 **kwargs
                 ):
        if multiplier < 0:
            raise ValueError("Multiplier must be positive")

        super().__init__(
            parent=camera.ui,
            position=Vec2(0.5, 0.5),
            origin=Vec2(0.5, 0.5),
            **kwargs
        )
        self.score = 0
        self.pacgum_eaten = 0
        self.pacgum_score = pacgum_score
        self.super_pacgum_eaten = 0
        self.super_pacgum_score = super_pacgum_score
        self.ghost_eaten = 0
        self.ghost_score = ghost_score
        self.lives = lives
        self.death = 0
        self.malus_death = malus_death
        self.time = time
        self.time_left = time
        self.multiplier = multiplier

        self.engine = game_engine

    def eat_pacgum(self):
        self.pacgum_eaten += 1
        self.score += self.pacgum_score * self.multiplier

    def eat_super_pacgum(self):
        self.super_pacgum_eaten += 1
        self.score += self.super_pacgum_score * self.multiplier

    def eat_ghost(self):
        self.ghost_eaten += 1
        self.score += self.ghost_score * self.multiplier

    def lose_life(self):
        self.lives -= 1
        self.score -= self.malus_death * self.multiplier

    def display_layout(self):
        TextUtils(
            text=(f"Score: {self.score}\n"
                  f"Lives: {self.lives}\n"
                  f"Pacgum eaten: {self.pacgum_eaten}\n"
                  f"Super pacgum eaten: {self.super_pacgum_eaten}\n"
                  f"Death: {self.death}\n"
                  f"Time: {self.time_left}\n"),
            position=Vec2(-0.05, -0.05),
            color=color.white,
            parent=self,
            origin=Vec2(0.5, 0.5),
        )
