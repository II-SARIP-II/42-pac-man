from ursina import Entity, Button, Vec3, color
from .EnumScene import EnumScene
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class MenuScene(Entity):
    def __init__(self, game_state: "GameEngine"):
        super().__init__()

        self.game_state = game_state

        Entity(model='plane',
               scale=Vec3(20, 1, 20),
               position=Vec3(0, 0, 0),
               color=color.orange,
               collider='box',
               parent=self
               )

        self.button_game = Button(
                model='plane',
                text='game',
                scale=Vec3(5, 1, 5),
                position=Vec3(0, 1, 0),
                color=color.blue,
                collider='box',
                parent=self
                )

        self.button_game.on_click = (
            lambda: self.game_state.display_scene(EnumScene.GAME))
