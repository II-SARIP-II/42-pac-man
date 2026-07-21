from typing import TYPE_CHECKING, Callable

from ursina import Button, Vec3, color

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class ButtonUtils(Button):
    """A pre-styled clickable button used across the game's UI scenes."""

    def __init__(
        self,
        text: str,
        action: Callable,
        parent: "GameScene",
        position: Vec3 = Vec3(0, 0, 0),
        scale: Vec3 = Vec3(5, 1, 1.5),
        button_color: color = color.blue,
    ) -> None:
        """Initialize the button and orient its label for the top-down camera.

        Args:
            text (str): Button label.
            action (Callable): Click callback.
            parent (GameScene): Scene to parent this button to.
            position (Vec3): World position.
            scale (Vec3): Button size.
            button_color (color): Background color.

        Returns:
            None.
        """
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
