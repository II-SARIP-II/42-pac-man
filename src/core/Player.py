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
    def __init__(
            self,
            parent: "GameScene",
            game_data: GameData,
            width: int,
            height: int
            ) -> None:

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
        self.position = convertPosToVec(
            self.start_pos,
            (self.width, self.height)
            )
        self.current_node = self.getNode(self.start_pos)
        self.target_node = self.current_node

        if not self.get_eaten:
            self.flashingPlayer()

    def getPlayerPos(self) -> Vec3:
        return self.get_position(relative_to=self.game_scene)

    def flashingPlayer(
            self,
            duration: float = 2.0,
            interval: float = 0.15
            ) -> None:

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
        opposite_direction = (self.current_direction + 2) % 4

        if self.wish_direction == opposite_direction:
            tmp = self.target_node
            self.target_node = self.current_node
            self.current_node = tmp
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
        self.game_data.eatGhost()
