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

    def update(self) -> None:
        if self.current_node == self.target_node and self.wish_direction >= 0:
            neighbour_coo = self.current_node.neighbours[self.wish_direction]
            if neighbour_coo is not None:
                neighbour = self.getNode(neighbour_coo)
                self.target_node = neighbour

        if self.current_node != self.target_node:
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

    # def goUp(self) -> None:
    #     self.position += Vec3(0, 0, 1)
    #     print(self.getPlayerPos())

    # def goDown(self) -> None:
    #     self.position += Vec3(0, 0, -1)
    #     print(self.getPlayerPos())

    # def goLeft(self) -> None:
    #     self.position += Vec3(-1, 0, 0)
    #     print(self.getPlayerPos())

    # def goRight(self) -> None:
    #     self.position += Vec3(1, 0, 0)
    #     print(self.getPlayerPos())

    def getPlayerPos(self) -> Vec3:
        return self.get_position(relative_to=self.game)

    # def eatItem(self, item: Item, game: GameScene) -> None:
    #     game.player_eat_item(item)
