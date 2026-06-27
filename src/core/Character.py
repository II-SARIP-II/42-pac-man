from ursina import Entity, Vec3, color


class Character(Entity):
    def __init__(
        self,
        model: str,
        scale: Vec3 = Vec3(0.5, 0.5, 0.5),
        collider: str = "box",
        position: Vec3 = Vec3(0, 0, 0),
        parent=None,
        color=color.yellow,
    ):
        super().__init__(
            model=model,
            scale=Vec3(0.5, 0.5, 0.5),
            collider="box",
            position=Vec3(0, 0, 0),
            parent=parent,
            color=color,
        )

    def move(self, direction: str) -> None:
        pass

    def resetPos(self) -> None:
        pass

    def respawn(self) -> None:
        pass

    def die(self) -> None:
        pass
