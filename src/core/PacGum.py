from typing import TYPE_CHECKING

from ursina import Vec3, color, time

from src.core.Item import Item

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class PacGum(Item):
    """A basic collectible pellet worth a small amount of points."""

    def __init__(
        self,
        score: int,
        position: Vec3,
        parent: "GameScene"
    ) -> None:
        """Initialize a standard pac-gum pellet.

        Args:
            score (int): Points awarded when eaten.
            position (Vec3): World position.
            parent (GameScene): Scene to parent this pellet to.

        Returns:
            None.
        """
        super().__init__(
            score=score,
            position=position,
            parent=parent,
            scale=Vec3(0.2, 0.2, 0.2)
        )


class SuperPacGum(Item):
    """A power pellet that grants the player temporary hunter status."""

    def __init__(
        self,
        score: int,
        position: Vec3,
        parent: "GameScene"
    ) -> None:
        """Initialize a super pac-gum power pellet.

        Args:
            score (int): Points awarded when eaten.
            position (Vec3): World position.
            parent (GameScene): Scene to parent this pellet to.

        Returns:
            None.
        """
        super().__init__(
            score=score,
            position=position,
            parent=parent,
            scale=Vec3(0.4, 0.4, 0.4)
        )

        self.flashing = 0
        self.speed = 0.1
        self.chrono = 0

    def update(self) -> None:
        """Update the pellet's flashing animation.

        Returns:
            None.
        """
        self.flashingEffect()

    def flashingEffect(self) -> None:
        """Toggle the pellet's color at a fixed interval.

        Returns:
            None.
        """
        self.chrono += time.dt

        if self.chrono >= self.speed:
            if self.flashing == 0:
                self.color = color.black
                self.flashing = 1
            else:
                self.color = color.salmon
                self.flashing = 0

            self.chrono = 0
