from ursina import Vec3, color
from typing import TYPE_CHECKING
import time

from src.core.Character import Character
from src.core.Node import Node
from src.utils import convertPosToVec

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Player(Character):
    def __init__(self, parent: "GameScene", width: int, height: int) -> None:
        super().__init__(
            model="sphere",
            scale=Vec3(0.5, 0.5, 0.5),
            collider="box",
            position=convertPosToVec((0, 0), (width, height)),
            color=color.yellow,
            parent=parent,
        )

        self.lives = 3
        self.scores = 0
        self.game = parent
        self.size = width, height

        self.position = convertPosToVec((0, 0), self.size)

        self.current_node = self.getNode((0, 0))
        self.target_node = self.current_node
        self.speed = 5.0
        self.wish_direction: int = -1
        self.current_direction: int = self.wish_direction

    def update(self) -> None:
        if self.current_node == self.target_node and self.wish_direction >= 0:

            self.current_direction = self.wish_direction

            wish_dir_neighbour = self.current_node.neighbours[self.wish_direction]

            if wish_dir_neighbour is not None:
                neighbour = self.getNode(wish_dir_neighbour)
                self.target_node = neighbour

            elif wish_dir_neighbour is None:
                print("oui ici la !!!!!!!!!!!!!!!!!!!!!!1")
                curr_dir_neighbour = self.current_node.neighbours[self.current_direction]
                if curr_dir_neighbour is not None:
                    self.target_node = curr_dir_neighbour

        if self.current_node != self.target_node:
            opposite_direction = (self.current_direction + 2) % 4

            if self.wish_direction == opposite_direction:
                self.target_node, self.current_node = self.current_node, self.target_node
                self.current_direction = self.wish_direction

            target_vector = convertPosToVec(self.target_node.pos, self.size)
            vector_to_target = target_vector - self.position

            direction = vector_to_target.normalized()
            distance_left = vector_to_target.length()

            step =self.speed * time.dt

            if distance_left <= step:
                self.position = target_vector
                self.current_node = self.target_node
            else:
                self.position += direction * step

    def getNode(self, coo: tuple[int, int]) -> Node:
        return self.game.level.level_map[coo]

    def loseLife(self) -> None:
        if self.lives > 0 and self.lives <= 3:
            self.lives -= 1

        if self.lives == 0:
            print("game over")

    def getPlayerPos(self) -> Vec3:
        return self.get_position(relative_to=self.game)

    # def eatItem(self, item: Item, game: GameScene) -> None:
    #     game.player_eat_item(item)
