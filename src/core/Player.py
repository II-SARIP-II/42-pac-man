from typing import TYPE_CHECKING

from ursina import Vec3, color, destroy, time, invoke

from src.core.Character import Character
from src.core.Node import Node
from src.GameData import GameData
from src.core.PacGum import SuperPacGum
from src.utils import convertPosToVec
from datetime import datetime

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Player(Character):
    """The player-controlled Pac-Man character."""

    def __init__(
            self,
            parent: "GameScene",
            game_data: GameData,
            width: int,
            height: int
            ) -> None:
        """Initialize the player at the center of the maze.

        Args:
            parent (GameScene): Scene to parent the player to.
            game_data (GameData): Score/lives/time tracker.
            width (int): Level grid width.
            height (int): Level grid height.

        Returns:
            None.
        """
        if width % 2 != 0:
            self.start_pos = (width // 2, height // 2)
        else:
            self.start_pos = (width // 2 - 1, height // 2)

        super().__init__(
            model="sphere",
            scale=Vec3(0.7, 0.7, 0.7),
            collider="box",
            texture=None,
            position=convertPosToVec(self.start_pos, (width, height)),
            color=color.yellow,
            parent=parent,
            width=width,
            height=height,
        )
        self.width = width
        self.height = height
        self.current_node = self.getNode(self.start_pos)
        self.target_node = self.current_node
        self.score = 0
        self.game_scene = parent
        self.game_data = game_data

        self.invincibility = False
        self.get_eaten = False
        self.is_hunter = False
        self.time_hunter: datetime | None = None

    def loseLife(self) -> None:
        """Reset the player's position after losing a life.

        Returns:
            None.
        """
        self.position = convertPosToVec(
            self.start_pos,
            (self.width, self.height)
            )
        self.current_node = self.getNode(self.start_pos)
        self.target_node = self.current_node

        if not self.get_eaten:
            self.flashingPlayer()

    def getPlayerPos(self) -> Vec3:
        """Get the player's position relative to the game scene.

        Returns:
            Vec3: Position relative to the parent `GameScene`.
        """
        return self.get_position(relative_to=self.game_scene)

    def flashingPlayer(
            self,
            duration: float = 2.0,
            interval: float = 0.15
            ) -> None:
        """Play a blinking animation indicating the player has died.

        Args:
            duration (float): Total animation length, in seconds.
            interval (float): Delay between color toggles, in seconds.

        Returns:
            None.
        """
        self.get_eaten = True

        max_steps = int(duration/interval)

        def toggle_color(step: int) -> None:
            if step >= max_steps:
                self.color = color.yellow
                self.get_eaten = False
                return

            self.color = color.yellow if step % 2 == 0 else color.black

            invoke(toggle_color, step + 1, delay=interval)

        toggle_color(0)

    def _handleDirectionChange(self) -> None:
        """Pick the next target node once the player reaches a node.

        Returns:
            None.
        """
        if self.wish_direction >= 0:
            wish_dir_neighbour = self.current_node.neighbours[
                self.wish_direction
                ]

            if wish_dir_neighbour is not None:
                self.current_direction = self.wish_direction
                neighbour = self.getNode(wish_dir_neighbour)
                self.target_node = neighbour

            elif wish_dir_neighbour is None:
                curr_dir_neighbour = self.current_node.neighbours[
                    self.current_direction
                ]
                if curr_dir_neighbour is not None:
                    neighbour = self.getNode(curr_dir_neighbour)
                    self.target_node = neighbour

    def _handleMovement(self) -> None:
        """Move the player one step towards its current target node.

        Returns:
            None.
        """
        opposite_direction = (self.current_direction + 2) % 4

        if self.wish_direction == opposite_direction:
            self.target_node = self.current_node
            self.current_direction = self.wish_direction

        target_vector = convertPosToVec(self.target_node.pos, self.size)
        vector_to_target = target_vector - self.position

        if vector_to_target and vector_to_target.length_squared() > 0:
            direction = vector_to_target.normalized()
            distance_left = vector_to_target.length()

            step = self.speed * time.dt

            if distance_left <= step:
                self.position = target_vector
                self.current_node = self.target_node
            else:
                self.position += direction * step

    def update(self) -> None:
        """Advance the player's state for the current frame.

        Returns:
            None.
        """
        if self.game_data.game_time <= 1:
            self.parent.gameLoose()
        if self.is_hunter and self.time_hunter:
            if (datetime.now() - self.time_hunter).total_seconds() > 5.0:
                self.is_hunter = False
                self.time_hunter = None

        if self.current_node.item:
            self.eatItem(self.current_node)

        if self.current_node == self.target_node:
            self._handleDirectionChange()
        else:
            self._handleMovement()

    def eatItem(self, node: Node) -> None:
        """Consume the item on the given node, if any.

        Args:
            node (Node): Maze node whose item should be eaten.

        Returns:
            None.
        """
        if node.item:
            self.game_data.addScore(node.item.score)
            if isinstance(node.item, SuperPacGum):
                self.is_hunter = True
                self.time_hunter = datetime.now()
            destroy(node.item)
            node.item = None
            self.game_scene.current_nb_pacgum -= 1
            self.game_scene.isTheLevelFinished()

    def eatGhost(self) -> None:
        """Award the player for eating a ghost while in hunter mode.

        Returns:
            None.
        """
        self.game_data.eatGhost()
