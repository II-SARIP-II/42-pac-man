from src.models.highscore import ScoresList
from src.scene.GameScene import GameScene
from src.utils_io import load_json_file
from src.core.Level import Level
from src.core.LevelGenerator import LevelGenerator
from typing import List
from ursina import Ursina, camera
from src.models.config import LevelValidation
from src.scene.EnumScene import EnumScene
from src.scene.MenuScene import MenuScene


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

        self.app = Ursina()
        camera.position = (0, 50, 0)
        camera.rotation_x = 90
        camera.rotation_y = 0
        camera.rotation_z = 0

        self.state = EnumScene.MENU

        self.game_scene = GameScene()
        self.game_scene.createMap(self.levels[0])
        self.game_scene.disable()

        self.menu_scene = MenuScene()
        self.current_scene = self.menu_scene

        self.menu_scene.button_game.on_click = lambda: self.display_scene(EnumScene.GAME)

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

    def display_scene(self, enum: EnumScene) -> None:
        if self.current_scene:
            self.current_scene.disable()

        self.state = enum
        print(self.state)

        if self.state == EnumScene.MENU:
            self.current_scene = self.menu_scene
            self.menu_scene.enable()
        elif self.state == EnumScene.GAME:
            self.current_scene = self.game_scene
            self.game_scene.enable()

        print(self.state)

    def game(self) -> None:
        self.app.run()
