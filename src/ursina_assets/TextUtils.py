from typing import TYPE_CHECKING, Any

from ursina import Text, Vec3, color

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class TextUtils(Text):
    """A pre-styled text label oriented for the game's top-down camera."""

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
        """Initialize the text label and orient it for the top-down camera.

        Args:
            parent (GameScene): Scene to parent this text to.
            text (str): Text content.
            position (Vec3): World position.
            color (color): Text color.
            origin (tuple[float, float]): Anchor point for positioning.
            scale (float): Text size.
            **kwargs (Any): Extra keyword arguments for the `Text` entity.

        Returns:
            None.
        """
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
