from ursina import Entity, Button, Vec3, color
from .EnumScene import EnumScene

class MenuScene(Entity):
    def __init__(self):
        super().__init__()
        from src.GameState import GameState

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
