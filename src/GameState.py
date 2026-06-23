from src.models.highscore import ScoresList
from src.utils_io import load_json_file
from src.core.Level import Level
from src.core.LevelGenerator import LevelGenerator
from typing import List
from ursina import Ursina, Entity, Vec3, color, camera
from src.models.config import LevelValidation


class GameState():
    def __init__(self,
                 highscore_filename: str,
                 levels: List[LevelValidation],
                 lives: int,
                 points_per_pacgum: int,
                 points_per_ghost: int,
                 seed: int,
                 level_max_time: int
                 ) -> None:
        self.highscore_filename_config = highscore_filename
        self.levels_config = levels
        self.lives_config = lives
        self.points_per_pacgum_config = points_per_pacgum
        self.points_per_ghost_config = points_per_ghost
        self.seed_config = seed
        self.level_max_time_config = level_max_time
        self.levels: List[Level] = self._getLevels(self.levels_config)
        try:
            self.scores = self._getScores(self.highscore_filename_config)
        except Exception as e:
            print(e)
        print(self.levels[0].level_map)
        print("\n\n", self.scores)
        self.game()

    @staticmethod
    def _getScores(filename: str) -> ScoresList:
        return ScoresList(**load_json_file(filename))

    @staticmethod
    def _getLevels(levels_config: List[LevelValidation]) -> List[Level]:
        levels: List[Level] = []
        for level in levels_config:
            levels.append(LevelGenerator().generate_level(level))
        return levels

    @staticmethod
    def createMap(mapData: Level) -> None:
        Entity(model='plane',
               scale=Vec3(mapData.width, 0, mapData.height),
               position=(0, 0, 0),
               color=color.black,
               collider='box'
               )
        Entity(model='plane',
               scale=Vec3(1, 0, 1),
               position=(0, 1, 0),
               color=color.yellow,
               collider='box'
               )
        for node in mapData.level_map.values():
            cell_x = node.pos[0] - (mapData.width / 2) + 0.5
            cell_z = -(node.pos[1] - (mapData.height / 2) + 0.5)
            if not node.get_neighbour(0):
                Entity(
                    model='cube', scale=Vec3(1, 2, 0.1),
                    position=(cell_x, 0.5, cell_z + 0.5),
                    color=color.blue, collider='box'
                )

            if not node.get_neighbour(1):
                Entity(
                    model='cube', scale=Vec3(0.1, 2, 1),
                    position=(cell_x + 0.5, 0.5, cell_z),
                    color=color.blue, collider='box'
                )

            if not node.get_neighbour(2):
                Entity(
                    model='cube', scale=Vec3(1, 2, 0.1),
                    position=(cell_x, 0.5, cell_z - 0.5),
                    color=color.blue, collider='box'
                )

            if not node.get_neighbour(3):
                Entity(
                    model='cube', scale=Vec3(0.1, 2, 1),
                    position=(cell_x - 0.5, 0.5, cell_z),
                    color=color.blue, collider='box'
                )

    def game(self) -> None:
        app = Ursina()
        self.createMap(self.levels[0])
        camera.position = (0, 50, 0)
        camera.rotation_x = 90
        camera.rotation_y = 0
        camera.rotation_z = 0
        app.run()
