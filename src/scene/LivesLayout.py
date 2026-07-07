from ursina import color, Vec2, Entity, camera, destroy, Text
from typing import Any

from src.GameData import GameData


class LivesLayout(Entity):
    def __init__(self,
                 game_data: GameData,
                 **kwargs: Any
                 ):
        super().__init__(
            parent=camera.ui,
            position=Vec2(-0.85, -0.45),
            origin=Vec2(-0.5, -0.5),
            **kwargs
        )
        self.game_data = game_data
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

        if self.game_data.lives > 9:
            life_icon = Entity(
                model="quad",
                scale=(0.05, 0.05),
                position=Vec2(0.06, 0),
                texture="assets/images/pacman.png",
                parent=self,
                color=color.yellow,
            )
            self.life_entities.append(life_icon)
            self.text_entity.text = f"x{self.game_data.lives}"

        else:
            self.text_entity.text = ""
            for i in range(self.game_data.lives):
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
