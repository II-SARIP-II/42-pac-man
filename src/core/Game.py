from Item import Item


class Game():
    def __init__(self) -> None:
        self.scores = 0
        self.levels = 0

    def player_eat_item(self, item: Item) -> None:
        self.scores += item.score
