from typing import Callable

from ursina import Button, Vec3, color


class ButtonUtils(Button):
    def __init__(
        self,
        text: str,
        position: Vec3,
        action: Callable,
        button_color=color.blue,
        parent_scene=None,
    ) -> None:

        super().__init__(
            model="plane",
            text=text,
            scale=Vec3(5, 1, 2),
            position=position,
            collider="box",
            parent=parent_scene,
            color=button_color,
        )

        if self.text_entity:
            self.text_entity.color = color.yellow
            self.text_entity.rotation_x = 90
            self.text_entity.y = 0.05

        self.on_click = action
