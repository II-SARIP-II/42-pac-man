from typing import List

from ursina import camera
# from ursina.scripts.smooth_follow import player

from src.core.Level import Level
from src.core.LevelGenerator import LevelGenerator
from src.models.config import LevelValidation
from src.models.highscore import ScoresList, Score
from src.scene.EnumScene import EnumScene
from src.scene.GameScene import GameScene
from src.scene.LoseScene import LoseScene
from src.scene.MenuScene import MenuScene
from src.scene.PauseScene import PauseScene
from src.scene.WinScene import WinScene
from src.scene.FinishScene import FinishScene
from src.scene.LeaderboardScene import LeaderboardScene
from src.scene.TextLayout import TextLayout
from src.scene.LivesLayout import LivesLayout
from src.utils_io import load_json_file, write_json_file
import json
from datetime import datetime


class GameEngine:
    def __init__(
        self,
        highscore_filename: str,
        levels: List[LevelValidation],
        lives: int,
        points_per_pacgum: int,
        points_per_super_pacgum: int,
        points_per_ghost: int,
        seed: int,
        level_max_time: int,
    ) -> None:

        self.highscore_filename_config = highscore_filename
        self.levels_config = levels
        self.lives_config = lives
        self.points_per_pacgum_config = points_per_pacgum
        self.points_per_super_pacgum_config = points_per_super_pacgum
        self.points_per_ghost_config = points_per_ghost
        self.seed_config = seed
        self.level_max_time_config = level_max_time

        self.levels: List[Level] = self._getLevels(self.levels_config)
        self.no_level = 0
        self.nb_level = len(self.levels) - 1

        self.current_score = 0

        # Additionnal Data
        self.death_malus = 100
        self.kill = 0

        self._setupEngine()

    def _setupEngine(self) -> None:
        # try:
        self.highscores = self._getScores(self.highscore_filename_config)

        camera.position = (0, 50, 0)
        camera.rotation = (90, 0, 0)

        self.state = EnumScene.MENU

        self.game_scene = GameScene(self, self.levels[self.no_level])
        self.game_scene.disable()

        self.pause_scene = PauseScene(self)
        self.pause_scene.disable()

        self.text_layout = TextLayout(
            self,
            self.level_max_time_config,
            1)
        self.text_layout.disable()

        self.lives_layout = LivesLayout(
            self,
            self.lives_config)
        self.lives_layout.disable()

        self.menu_scene = MenuScene(self)
        self.current_scene = self.menu_scene
        # except Exception as e:
        #     raise ValueError(e)

    @staticmethod
    def _getScores(filename: str) -> ScoresList:
        try:
            return ScoresList(**load_json_file(filename))
        except (ValueError, FileNotFoundError):
            print(f"{filename} was empty or invalid.")
            return ScoresList(scores=[])

    @staticmethod
    def _getLevels(levels_config: List[LevelValidation]) -> List[Level]:
        levels: List[Level] = []
        for level in levels_config:
            levels.append(LevelGenerator().generateLevel(level))
        return levels

    def quitGame(self) -> None:
        quit()

    def displayScene(self, enum: EnumScene) -> None:
        self.text_layout.disable()
        self.lives_layout.disable()
        if self.current_scene:
            self.current_scene.disable()

        self.state = enum

        if self.state == EnumScene.MENU:
            self.current_scene = self.menu_scene
            self.menu_scene.enable()
        elif self.state == EnumScene.GAME:
            self.current_scene = self.game_scene
            self.game_scene.enable()
            self.text_layout.enable()
            self.lives_layout.enable()
        elif self.state == EnumScene.PAUSE:
            self.current_scene = self.pause_scene
            self.pause_scene.enable()
        elif self.state == EnumScene.LOSE:
            self.lose_scene = LoseScene(self)
            self.current_scene = self.lose_scene
            self.lose_scene.enable()
        elif self.state == EnumScene.WIN:
            self.win_scene = WinScene(self)
            self.current_scene = self.win_scene
            self.win_scene.enable()
        elif self.state == EnumScene.FINISH:
            self.finish_scene = FinishScene(self)
            self.current_scene = self.finish_scene
            self.finish_scene.enable()
        elif self.state == EnumScene.HIGHSCORE:
            self.highscores = self._getScores(self.highscore_filename_config)
            self.highscore_scene = LeaderboardScene(self, self.highscores)
            self.current_scene = self.highscore_scene
            self.highscore_scene.enable()

    def nextLevel(self) -> None:
        if self.no_level <= self.nb_level:
            self.game_scene = GameScene(self, self.levels[self.no_level])
            self.game_scene.disable()
            self.displayScene(EnumScene.GAME)
        else:
            self.displayScene(EnumScene.FINISH)

    def eatPacgum(self) -> None:
        self.current_score += self.points_per_pacgum_config

    def eatSuperPacgum(self) -> None:
        self.current_score += self.points_per_super_pacgum_config

    def eatGhost(self) -> None:
        self.current_score += self.points_per_ghost_config
        self.kill += 1

    def loseLife(self) -> None:
        self.lives_config -= 1
        self.lives_layout.loseLife()
        self.text_layout.add_death()
        self.current_score -= self.death_malus

    def submitScore(self) -> None:
        name = self.finish_scene.player_name.text.strip()
        if not name:
            print("The name cannot be empty.")
            return

        self.write_highscore(name)
        self.displayScene(EnumScene.MENU)

    def write_highscore(self, name: str) -> None:
        game_score = Score(
            name=name,
            score=self.current_score,
            date=datetime.now()
            )
        self.highscores.scores.append(game_score)
        self.highscores.scores = sorted(
            self.highscores.scores,
            key=lambda x: x.score,
            reverse=True
            )[:10]
        clean_dict = json.loads(self.highscores.model_dump_json())
        write_json_file(clean_dict, "config/highscores.json")

    def infiniteLive(self) -> None:
        self.lives_layout.infiniteLive()
