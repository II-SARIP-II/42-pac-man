from ursina import Vec3, color

from src.core.Character import Character
from src.utils import convertPosToVec
from typing import TYPE_CHECKING

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
            width=width,
            height=height
        )

        self.lives = 3
        self.scores = 0

    def loseLife(self) -> None:
        if self.lives > 0 and self.lives <= 3:
            self.lives -= 1

        if self.lives == 0:
            print("game over")

    def getPlayerPos(self) -> Vec3:
        return self.get_position(relative_to=self.game_scene)

    # def eatItem(self, item: Item, game: GameScene) -> None:
    #     game.player_eat_item(item)
