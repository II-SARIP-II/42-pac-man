from src.models.highscore import ScoresList
from src.utils_io import load_json_file
from src.core.Level import Level
from src.core.LevelGenerator import LevelGenerator
from typing import List

class GameState():
    def __init__(self,
                 highscore_filename,
                 levels,
                 lives,
                 points_per_pacgum,
                 points_per_ghost,
                 seed,
                 level_max_time
                 ):
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

    @staticmethod
    def _getScores(filename: str):
        return ScoresList(**load_json_file(filename))

    @staticmethod
    def _getLevels(levels_config) -> List[Level]:
        levels: List[Level] = []
        for level in levels_config:
            levels.append(LevelGenerator().generate_level(level))
        return levels
