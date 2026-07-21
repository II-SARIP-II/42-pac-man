from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

from src.core.Node import Node

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Character(Entity):
    """Base class for moving actors in the game (player and ghosts)."""

    def __init__(
        self,
        model: str,
        width: int,
        height: int,
        parent: "GameScene",
        texture: str | None,
        scale: Vec3 = Vec3(0.5, 0.5, 0.5),
        collider: str = "box",
        position: Vec3 = Vec3(0, 0, 0),
        color: color = color.yellow,
    ) -> None:
        """Initialize the character's entity and movement state.

        Args:
            model (str): 3D model name.
            width (int): Level grid width.
            height (int): Level grid height.
            parent (GameScene): Scene to parent this entity to.
            texture (str | None): Texture path, if any.
            scale (Vec3): Entity size.
            collider (str): Collider shape.
            position (Vec3): Initial world position.
            color (color): Tint color.

        Returns:
            None.
        """
        super().__init__(
            model=model,
            scale=scale,
            collider="box",
            position=position,
            texture=texture,
            parent=parent,
            color=color,
        )

        self.size = width, height
        self.game_scene = parent

        self.position = position

        self.speed = 5.0
        self.wish_direction: int = -1
        self.current_direction: int = self.wish_direction

    def move(self, direction: str) -> None:
        """Move the character. Overridden by subclasses.

        Args:
            direction (str): Direction to move in.

        Returns:
            None.
        """
        pass

    def resetPos(self) -> None:
        """Reset the character's position. Overridden by subclasses.

        Returns:
            None.
        """
        pass

    def respawn(self) -> None:
        """Respawn the character. Overridden by subclasses.

        Returns:
            None.
        """
        pass

    def die(self) -> None:
        """Handle death. Overridden by subclasses.

        Returns:
            None.
        """
        pass

    def update(self) -> None:
        """Update per-frame state. Overridden by subclasses.

        Returns:
            None.
        """
        pass

    def getNode(self, coo: tuple[int, int]) -> Node:
        """Look up the maze `Node` at a grid coordinate.

        Args:
            coo (tuple[int, int]): Grid coordinate to look up.

        Returns:
            Node: The node at that coordinate.
        """
        return self.game_scene.level.level_map[coo]
