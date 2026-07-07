from typing import TYPE_CHECKING

from ursina import Vec3, color, destroy, time

from src.core.Character import Character
from src.core.Node import Node
from src.utils import convertPosToVec

if TYPE_CHECKING:
    from src.scene.GameScene import GameScene


class Player(Character):
    def __init__(self, parent: "GameScene", width: int, height: int) -> None:
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
        self.get_eaten = False

    def loseLife(self) -> None:
        self.position = convertPosToVec(self.start_pos, (self.width, self.height))
        self.current_node = self.getNode(self.start_pos)
        self.target_node = self.current_node
        self.get_eaten = True

    def getPlayerPos(self) -> Vec3:
        return self.get_position(relative_to=self.game_scene)

    def flashingPlayer(self, duration=3.0, interval=0.2):
        self.get_eaten = False
        light_yellow = color.rgb32(246, 255, 205)
        original_color = color.yellow

        def toggle_color(step):
            if step >= duration / interval:
                self.color = original_color
                return
            if self.color == light_yellow:
                self.color = original_color
            else:
                self.color = light_yellow

            from ursina import invoke
            invoke(toggle_color, step + 1, delay=interval)
        toggle_color(0)

    def update(self) -> None:
        if self.get_eaten:
            self.flashingPlayer()

        if self.current_node.item:
            self.eatItem(self.current_node)

        if self.current_node == self.target_node:
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

        if self.current_node != self.target_node:
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

    def eatItem(self, node: Node) -> None:
        if node.item:
            self.game_scene.game_engine.current_score += node.item.score
            destroy(node.item)
            node.item = None
            self.game_scene.current_nb_pacgum -= 1
            self.game_scene.isTheLevelFinished()
