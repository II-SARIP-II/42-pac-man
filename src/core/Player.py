from Item import Item
from Game import Game
from Character import Character


class Player(Character):
    def __init__(self) -> None:
        self.lives = 3
        self.scores = 0

    def lose_life(self) -> None:
        if self.lives > 0 and self.lives <= 3:
            self.lives -= 1

        if self.lives == 0:
            print("game over")

    def eat_item(self, item: Item, game: Game) -> None:
        game.player_eat_item(item)
