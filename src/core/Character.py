from ursina import Entity


class Character(Entity):
    def __init__(self, model: str):
        super().__init__(model)

    def move(self, direction: str) -> None:
        pass

    def resetPos(self) -> None:
        pass

    def respawn(self) -> None:
        pass

    def die(self) -> None:
        pass
