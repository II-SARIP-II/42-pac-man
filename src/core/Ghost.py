import random
from datetime import datetime, timedelta
from enum import Enum
from typing import TYPE_CHECKING, Any, List, Optional, Tuple
from src.core.Level import Level

from ursina import Vec3, color

from src.core.Character import Character
from src.core.Node import Node
from src.core.Player import Player
from src.utils import convertVecToPos, convertPosToVec

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class EnumMode(Enum):
    """AI states a `Ghost` can be in.

    Attributes:
        CHASE: Pursuing a per-subclass target position.
        RANDOM: Wandering towards a random tile.
        SCARED: Fleeing from the player.
        DEAD: Eaten, heading back to spawn.
        STOP: Frozen in place.
    """

    CHASE = 1
    RANDOM = 2
    SCARED = 3
    DEAD = 4
    STOP = 5


class Ghost(Character):
    """Base class for the AI-controlled enemies chasing the player.

    Handles the shared mode state machine, player collision, and BFS
    pathing. Subclasses implement `chaseMovement`, `deadMovement`,
    `moving`, and `bfs`.
    """

    def __init__(
        self,
        width: int,
        height: int,
        image_path: str,
        parent: "GameScene",
        player: Player,
        position: Vec3,
        spawn_pos: tuple[int, int],
        level: Level
    ) -> None:
        """Initialize the ghost's shared movement/AI state.

        Args:
            width (int): Level grid width.
            height (int): Level grid height.
            image_path (str): Texture for the ghost's normal appearance.
            parent (GameScene): Scene to parent this ghost to.
            player (Player): Player the ghost reacts to.
            position (Vec3): Initial world position.
            spawn_pos (tuple[int, int]): Grid coordinate to respawn at.
            level (Level): Level to navigate.

        Returns:
            None.
        """
        self.spawn_position = spawn_pos

        spawn_position = Vec3(position.x, 0.1, position.z)
        self.image = image_path
        super().__init__(
            model="quad",
            texture=image_path,
            width=width,
            height=height,
            parent=parent,
            scale=Vec3(0.6, 0.6, 0.6),
            color=color.white,
            position=spawn_position,
        )
        self.level = level
        self.rotation = Vec3(90, 0, 0)
        self.width = width
        self.height = height
        self.is_edible = False
        self.player = player
        self.frame_counter = 0
        self.speed = 2
        self.last_node: Optional[Node] = None
        self.mode = EnumMode.CHASE
        self.chase_count = 0
        self.target_path: List[Node] = []
        self.last_player_death = datetime.now()
        self.has_been_killed = False
        self.stop = False

    def respawn(self) -> None:
        """Reset the ghost to its spawn position and default state.

        Returns:
            None.
        """
        self.position = convertPosToVec(
            self.spawn_position, (self.width, self.height))

        self.mode = EnumMode.CHASE
        self.speed = 2
        self.chase_count = 0
        self.target_path = []
        self.last_node = None

        self.last_player_death = datetime.now()

    def update(self) -> None:
        """Advance the ghost's AI and movement for the current frame.

        Returns:
            None.
        """
        if self.mode == EnumMode.STOP:
            self.stop = True
        if not self.stop:
            if self.player.is_hunter:
                if self.mode != EnumMode.DEAD:
                    self.mode = EnumMode.SCARED
            else:
                self.has_been_killed = False
                if self.mode == EnumMode.SCARED:
                    self.mode = EnumMode.CHASE
                    self.texture = self.image

            if len(self.target_path) < 2:
                self.recalculatePath()

            arrive_au_node = self.moving()
            self.playerCollision()

            if arrive_au_node:
                if len(self.target_path) >= 2:
                    self.last_node = self.target_path[0]
                self.recalculatePath()

        else:
            if self.player.is_hunter:
                if self.mode != EnumMode.DEAD:
                    self.mode = EnumMode.SCARED
                    self.alpha = 1
                    self.texture = "assets/images/scared_ghost.png"
            else:
                self.has_been_killed = False
                if self.mode == EnumMode.SCARED:
                    self.mode = EnumMode.CHASE
                    self.texture = self.image
            self.playerCollision()

    def recalculatePath(self) -> None:
        """Recompute the target position and BFS path towards it.

        Returns:
            None.
        """
        if self.mode == EnumMode.CHASE:
            player_pos = self.player.getPlayerPos()
            player_grid_pos = convertVecToPos(
                player_pos,
                (self.width, self.height)
            )
            target_pos = self.chaseMovement(player_grid_pos)
        elif self.mode == EnumMode.RANDOM:
            target_pos = self.randomMovement()
        elif self.mode == EnumMode.SCARED:
            target_pos = self.scaredMovement()
        elif self.mode == EnumMode.DEAD:
            target_pos = self.deadMovement()
        else:
            return

        ghost_grid_pos = convertVecToPos(
            self.position,
            (self.width, self.height)
        )
        if (
            ghost_grid_pos in self.level.level_map
            and target_pos in self.level.level_map
        ):
            self.bfs(
                self.level.level_map[ghost_grid_pos],
                self.level.level_map[target_pos],
                self.last_node,
            )

    def getEaten(self) -> None:
        """Handle being eaten by the player. Overridden by subclasses.

        Returns:
            None.
        """
        pass

    def getTargetPos(self) -> Vec3:
        """Get the world position used as the chase reference.

        Returns:
            Vec3: The player's current world position.
        """
        return self.player.getPlayerPos()

    def randomMovement(self) -> Tuple[int, int]:
        """Compute a random target grid position for RANDOM mode.

        Returns:
            Tuple[int, int]: A random (x, y) grid position.
        """
        self.alpha: float = 1
        self.chase_count += 1
        if self.chase_count > 15:
            self.mode = EnumMode.CHASE
            self.chase_count = 0
        return (
            random.randint(0, self.width - 1),
            random.randint(0, self.height - 1),
        )

    def scaredMovement(self) -> Any:
        """Compute a flee target that maximizes distance from the player.

        Returns:
            Any: The neighbour grid position furthest from the player.
        """
        self.alpha = 1
        self.texture = "assets/images/scared_ghost.png"

        player_vec = self.getTargetPos()
        player_x, player_y = convertVecToPos(
            player_vec,
            (self.width, self.height)
        )
        ghost_grid_pos = convertVecToPos(
            self.position,
            (self.width, self.height)
        )
        current_node = self.level.level_map[ghost_grid_pos]
        best_pos = ghost_grid_pos
        max_distance = -1

        for neighbour_pos in current_node.neighbours:
            if neighbour_pos is None:
                continue

            nx, ny = neighbour_pos
            distance = abs(player_x - nx) + abs(player_y - ny)

            if distance > max_distance:
                max_distance = distance
                best_pos = neighbour_pos

        return best_pos

    def playerCollision(self) -> None:
        """Check for and resolve a collision with the player.

        Returns:
            None.
        """
        player_vec = self.getTargetPos()
        player_pos = convertVecToPos(player_vec, (self.width, self.height))
        ghost_pos = convertVecToPos(self.position, (self.width, self.height))

        if player_pos != ghost_pos:
            return

        if self.player.is_hunter:
            if self.mode != EnumMode.DEAD:
                self.getKilled()
        else:
            if self.mode == EnumMode.DEAD or self.player.invincibility:
                return

            grace_period = timedelta(seconds=2)
            if datetime.now() < self.last_player_death + grace_period:
                return

            self.last_player_death = datetime.now()
            self.parent.killPlayer()

    def getKilled(self) -> None:
        """Mark the ghost as killed and award the player.

        Returns:
            None.
        """
        self.mode = EnumMode.DEAD
        self.player.eatGhost()
        self.has_been_killed = True
        self.texture = self.image
        self.alpha = 0.5
