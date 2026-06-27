from ursina import Vec3, color

from src.core.Character import Character


class Player(Character):
    def __init__(self, parent) -> None:
        super().__init__(
            model="sphere",
            scale=Vec3(0.5, 0.5, 0.5),
            collider="box",
            position=Vec3(0, 0, 0),
            color=color.yellow,
            parent=parent,
        )
        self.lives = 3
        self.scores = 0
        self.game = parent

    def loseLife(self) -> None:
        if self.lives > 0 and self.lives <= 3:
            self.lives -= 1

        if self.lives == 0:
            print("game over")

    def goUp(self) -> None:
        self.position += Vec3(0, 0, 1)
        print(self.getPlayerPos())

    def goDown(self) -> None:
        self.position += Vec3(0, 0, -1)
        print(self.getPlayerPos())

    def goLeft(self) -> None:
        self.position += Vec3(-1, 0, 0)
        print(self.getPlayerPos())

    def goRight(self) -> None:
        self.position += Vec3(1, 0, 0)
        print(self.getPlayerPos())

    def getPlayerPos(self) -> Vec3:
        return self.get_position(relative_to=self.game)

    # def eatItem(self, item: Item, game: GameScene) -> None:
    #     game.player_eat_item(item)
