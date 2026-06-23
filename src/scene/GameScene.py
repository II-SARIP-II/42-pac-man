from ursina import Entity, Vec3, color
from src.core.Level import Level


class GameScene(Entity):
    def __init__(self) -> None:
        super().__init__()

    def createMap(self, level: Level) -> None:
        Entity(model='plane',
               scale=Vec3(level.width, 0, level.height),
               position=Vec3(0, 0, 0),
               color=color.black,
               collider='box',
               parent=self
               )
        Entity(model='plane',
               scale=Vec3(1, 0, 1),
               position=Vec3(0, 1, 0),
               color=color.yellow,
               collider='box',
               parent=self
               )
        for node in level.level_map.values():
            cell_x = node.pos[0] - (level.width / 2) + 0.5
            cell_z = -(node.pos[1] - (level.height / 2) + 0.5)
            if not node.get_neighbour(0):
                Entity(
                    model='cube', scale=Vec3(1, 2, 0.1),
                    position=Vec3(cell_x, 0.5, cell_z + 0.5),
                    color=color.blue, collider='box',
                    parent=self
                )

            if not node.get_neighbour(1):
                Entity(
                    model='cube', scale=Vec3(0.1, 2, 1),
                    position=Vec3(cell_x + 0.5, 0.5, cell_z),
                    color=color.blue, collider='box',
                    parent=self
                )

            if not node.get_neighbour(2):
                Entity(
                    model='cube', scale=Vec3(1, 2, 0.1),
                    position=Vec3(cell_x, 0.5, cell_z - 0.5),
                    color=color.blue, collider='box',
                    parent=self
                )

            if not node.get_neighbour(3):
                Entity(
                    model='cube', scale=Vec3(0.1, 2, 1),
                    position=Vec3(cell_x - 0.5, 0.5, cell_z),
                    color=color.blue, collider='box',
                    parent=self
                )
