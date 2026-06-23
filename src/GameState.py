from src.models.highscore import ScoresList
from src.scene.GameScene import GameScene
from src.utils_io import load_json_file
from src.core.Level import Level
from src.core.LevelGenerator import LevelGenerator
from typing import List
from ursina import Ursina, camera
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

    def game(self) -> None:
        app = Ursina()
        game_scene = GameScene()
        game_scene.createMap(self.levels[0])
        camera.position = (0, 50, 0)
        camera.rotation_x = 90
        camera.rotation_y = 0
        camera.rotation_z = 0
        app.run()
