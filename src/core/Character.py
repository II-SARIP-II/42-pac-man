from ursina import Entity, Vec3, color, time
from src.utils import convertPosToVec
from src.core.Node import Node
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Character(Entity):
    def __init__(
        self,
        model: str,
        width: int,
        height: int,
        parent: "GameScene",
        scale: Vec3 = Vec3(0.5, 0.5, 0.5),
        collider: str = "box",
        position: Vec3 = Vec3(0, 0, 0),
        color: color = color.yellow
    ):
        super().__init__(
            model=model,
            scale=Vec3(0.5, 0.5, 0.5),
            collider="box",
            position=Vec3(0, 0, 0),
            parent=parent,
            color=color,
        )

        self.size = width, height
        self.game_scene = parent

        self.position = convertPosToVec((0, 0), self.size)

        self.current_node = self.getNode((0, 0))
        self.target_node = self.current_node
        self.speed = 5.0
        self.wish_direction: int = -1
        self.current_direction: int = self.wish_direction

    def move(self, direction: str) -> None:
        pass

    def resetPos(self) -> None:
        pass

    def respawn(self) -> None:
        pass

    def die(self) -> None:
        pass

    def update(self) -> None:
        self.movement()

    def getNode(self, coo: tuple[int, int]) -> Node:
        return self.game_scene.level.level_map[coo]

    def movement(self) -> None:
        if self.current_node == self.target_node:
            if self.wish_direction >= 0:
                wish_dir_neighbour = self.current_node.neighbours[
                    self.wish_direction]

                if wish_dir_neighbour is not None:
                    self.current_direction = self.wish_direction
                    neighbour = self.getNode(wish_dir_neighbour)
                    self.target_node = neighbour

                elif wish_dir_neighbour is None:
                    curr_dir_neighbour = self.current_node.neighbours[
                        self.current_direction]
                    if curr_dir_neighbour is not None:
                        neighbour = self.getNode(curr_dir_neighbour)
                        self.target_node = neighbour

        if self.current_node != self.target_node:
            opposite_direction = (self.current_direction + 2) % 4

            if self.wish_direction == opposite_direction:
                print("bug")
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
