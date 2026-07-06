from typing import List

from ursina import camera

from src.core.Level import Level
from src.core.LevelGenerator import LevelGenerator
from src.models.config import LevelValidation
from src.models.highscore import ScoresList
from src.scene.EnumScene import EnumScene
from src.scene.GameScene import GameScene
from src.scene.LoseScene import LoseScene
from src.scene.MenuScene import MenuScene
from src.scene.PauseScene import PauseScene
from src.scene.WinScene import WinScene
from src.scene.Layout import Layout
from src.utils_io import load_json_file


class GameEngine:
    def __init__(
        self,
        highscore_filename: str,
        levels: List[LevelValidation],
        lives: int,
        points_per_pacgum: int,
        points_per_ghost: int,
        seed: int,
        level_max_time: int,
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
        # try:
        self.scores = self._getScores(self.highscore_filename_config)

        camera.position = (0, 50, 0)
        camera.rotation = (90, 0, 0)

        self.state = EnumScene.MENU

        self.game_scene = GameScene(self, self.levels[0])
        self.game_scene.disable()

        self.pause_scene = PauseScene(self)
        self.pause_scene.disable()

        self.win_scene = WinScene(self)
        self.win_scene.disable()

        self.lose_scene = LoseScene(self)
        self.lose_scene.disable()

        self.layout = Layout(
            self,
            self.lives_config,
            self.level_max_time_config,
            self.points_per_pacgum_config,
            self.points_per_pacgum_config*5,
            self.points_per_ghost_config, 100, 1
            )
        self.layout.disable()

        self.menu_scene = MenuScene(self)
        self.current_scene = self.menu_scene
        # except Exception as e:
        #     raise ValueError(e)

    @staticmethod
    def _getScores(filename: str) -> ScoresList:
        return ScoresList(**load_json_file(filename))

    @staticmethod
    def _getLevels(levels_config: List[LevelValidation]) -> List[Level]:
        levels: List[Level] = []
        for level in levels_config:
            levels.append(LevelGenerator().generateLevel(level))
        return levels

    def quitGame(self) -> None:
        quit()

    def displayScene(self, enum: EnumScene) -> None:
        self.layout.disable()
        if self.current_scene:
            self.current_scene.disable()

        self.state = enum

        if self.state == EnumScene.MENU:
            self.current_scene = self.menu_scene
            self.menu_scene.enable()
        elif self.state == EnumScene.GAME:
            self.current_scene = self.game_scene
            self.game_scene.enable()
            self.layout.enable()
        elif self.state == EnumScene.PAUSE:
            self.current_scene = self.pause_scene
            self.pause_scene.enable()
        elif self.state == EnumScene.LOSE:
            self.current_scene = self.lose_scene
            self.lose_scene.enable()
        elif self.state == EnumScene.WIN:
            self.current_scene = self.win_scene
            self.win_scene.enable()
