from ursina import Entity


class Character(Entity):
    def __init__(self, model):
        super().__init__(model)

    def move(self, direction: str) -> None:
        pass

    def reset_pos(self) -> None:
        pass

    def respawn(self) -> None:
        pass

    def die(self) -> None:
        pass
