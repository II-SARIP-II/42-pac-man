from ursina import Entity, Button, Vec3, color
from .EnumScene import EnumScene
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class MenuScene(Entity):
    def __init__(self, game_state: "GameEngine"):
        super().__init__()

        self.game_state = game_state
        self.createButtons()
        self.createBackground()

    def createBackground(self) -> None:
        Entity(model='plane',
               scale=Vec3(20, 1, 20),
               position=Vec3(0, 0, 0),
               color=color.black,
               collider='box',
               parent=self
               )

    def createButtons(self) -> None:
        self.buttonPlay()

    def buttonPlay(self) -> None:
        self.button_game = Button(
            model='plane',
            text='PLAY',
            scale=Vec3(5, 1, 2),
            position=Vec3(0, 1, 1),
            collider='box',
            parent=self,
            color=color.blue
            )

        if self.button_game.text_entity:
            self.button_game.text_entity.color = color.yellow
            self.button_game.text_entity.rotation_x = 90
            self.button_game.text_entity.y = 0.05

        self.button_game.on_click = (
            lambda: self.game_state.display_scene(EnumScene.GAME))
