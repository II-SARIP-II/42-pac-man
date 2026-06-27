from Character import Character
from Game import GameScene
from Item import Item


class Player(Character):
    def __init__(self) -> None:
        self.lives = 3
        self.scores = 0

    def loseLife(self) -> None:
        if self.lives > 0 and self.lives <= 3:
            self.lives -= 1

        if self.lives == 0:
            print("game over")

    def eatItem(self, item: Item, game: GameScene) -> None:
        game.player_eat_item(item)
