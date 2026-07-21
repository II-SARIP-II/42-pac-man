from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Item(Entity):
    """Base class for collectible entities placed on the maze grid."""

    def __init__(
        self,
        score: int,
        position: Vec3,
        parent: "GameScene",
        model: str = "sphere",
        scale: Vec3 = Vec3(0.5, 0.5, 0.5),
        collider: str = 'box',
        color: color = color.salmon
    ) -> None:
        """Initialize the item entity and its score value.

        Args:
            score (int): Points awarded when eaten.
            position (Vec3): World position.
            parent (GameScene): Scene to parent this item to.
            model (str): 3D model name.
            scale (Vec3): Item size.
            collider (str): Collider shape.
            color (color): Tint color.

        Returns:
            None.
        """
        super().__init__(
            model=model,
            scale=scale,
            collider=collider,
            position=position,
            parent=parent,
            color=color
        )

        self.score = score
        self.pos = position
