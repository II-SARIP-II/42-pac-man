from src.models.highscore import ScoresList
from src.scene.GameScene import GameScene
from src.utils_io import load_json_file
from src.core.Level import Level
from src.core.LevelGenerator import LevelGenerator
from typing import List
from ursina import camera
from src.models.config import LevelValidation
from src.scene.EnumScene import EnumScene
from src.scene.MenuScene import MenuScene


class GameEngine():
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

        self._setupEngine()

    def _setupEngine(self) -> None:
        try:
            self.scores = self._getScores(self.highscore_filename_config)

            camera.position = (0, 50, 0)
            camera.rotation = (90, 0, 0)

            self.state = EnumScene.MENU

            self.game_scene = GameScene(self)
            self.game_scene.createMap(self.levels[0])
            self.game_scene.disable()

            self.menu_scene = MenuScene(self)
            self.current_scene = self.menu_scene
        except Exception as e:
            raise ValueError(e)

    @staticmethod
    def _getScores(filename: str) -> ScoresList:
        return ScoresList(**load_json_file(filename))

    @staticmethod
    def _getLevels(levels_config: List[LevelValidation]) -> List[Level]:
        levels: List[Level] = []
        for level in levels_config:
            levels.append(LevelGenerator().generate_level(level))
        return levels

    def display_scene(self, enum: EnumScene) -> None:
        if self.current_scene:
            self.current_scene.disable()

        self.state = enum

        if self.state == EnumScene.MENU:
            self.current_scene = self.menu_scene
            self.menu_scene.enable()
        elif self.state == EnumScene.GAME:
            self.current_scene = self.game_scene
            self.game_scene.enable()
