from typing import TYPE_CHECKING

from ursina import Entity, Vec3, color

if TYPE_CHECKING:
    from src.GameEngine import GameEngine


class Scene(Entity):
    """Base class for every screen/scene managed by the `GameEngine`."""

    def __init__(self, game_engine: "GameEngine"):
        """Initialize the scene and store a reference to the engine.

        Args:
            game_engine (GameEngine): The engine managing scene
                transitions and shared game state.

        Returns:
            None.
        """
        super().__init__()

        self.game_engine = game_engine

    def createScene(self) -> None:
        """Build the scene's contents.

        Intended to be overridden by subclasses; the base implementation
        does nothing.

        Returns:
            None.
        """
        pass

    def createBackground(self) -> None:
        """Create the flat black background plane behind the scene.

        Returns:
            None.
        """
        Entity(
            model="plane",
            scale=Vec3(20, 1, 20),
            position=Vec3(0, 0, 0),
            color=color.black,
            collider="box",
            parent=self,
        )

    def onEntry(self) -> None:
        """Enable the scene when it becomes the active/current scene.

        Returns:
            None.
        """
        self.enable()

    def onExit(self) -> None:
        """Disable the scene when it stops being the active scene.

        Returns:
            None.
        """
        self.disable()
