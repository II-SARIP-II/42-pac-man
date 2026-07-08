from typing import TYPE_CHECKING, Any

from ursina import Text, Vec3, color

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class TextUtils(Text):
    def __init__(
        self,
        parent: "GameScene",
        text: str = "",
        position: Vec3 = Vec3(0, 0, 0),
        color: color = color.white,
        origin: tuple[float, float] = (0, 0),
        scale: float = 30,
        **kwargs: Any,
    ) -> None:

        super().__init__(
            text=text,
            position=position,
            color=color,
            parent=parent,
            origin=origin,
            scale=scale,
            **kwargs,
        )

        self.rotation_x = 90
        self.scale = scale
