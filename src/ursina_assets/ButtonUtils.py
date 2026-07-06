from typing import Callable

from ursina import Button, Vec3, color

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class ButtonUtils(Button):
    def __init__(
        self,
        text: str,
        action: Callable,
        parent: "GameScene",
        position: Vec3 = Vec3(0, 0, 0),
        scale: Vec3 = Vec3(5, 1, 1.5),
        button_color: color = color.blue,
    ) -> None:

        super().__init__(
            model="plane",
            text=text,
            scale=scale,
            position=position,
            collider="box",
            parent=parent,
            color=button_color,
        )

        if self.text_entity:
            self.text_entity.color = color.yellow
            self.text_entity.rotation_x = 90
            self.text_entity.y = 0.05

        self.on_click = action
