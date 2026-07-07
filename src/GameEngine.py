from typing import List

from ursina import camera

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

        self.levels: list[Level] = []
        self.no_level: int = 0
        self.nb_level: int = 0
        self.current_score: int = 0
        self.death_malus: int = 0
        self.kill: int = 0
        self.is_lose: bool = False

        self.resetGame()
        self._setupEngine()

    def _setupEngine(self) -> None:
        # try:
        self.highscores = self._getScores(self.highscore_filename_config)

        camera.position = (0, 50, 0)
        camera.rotation = (90, 0, 0)

        self.state = EnumScene.MENU

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

        self.win_scene = WinScene(self)
        self.win_scene.disable()

        self.lose_scene = LoseScene(self)
        self.lose_scene.disable()

        self.finish_scene = FinishScene(self)
        self.finish_scene.disable()

        self.highscore_scene = LeaderboardScene(self, self.highscores)
        self.highscore_scene.disable()

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
            self.resetGame()
        elif self.state == EnumScene.GAME:
            self.game_scene = GameScene(self, self.levels[self.no_level])
        elif self.state == EnumScene.HIGHSCORE:
            self.highscores = self._getScores(self.highscore_filename_config)

        scene_mapping = {
            EnumScene.MENU: (self.menu_scene, False),
            EnumScene.GAME: (self.game_scene, True),
            EnumScene.RESUME: (self.game_scene, True),
            EnumScene.PAUSE: (self.pause_scene, False),
            EnumScene.LOSE: (self.lose_scene, False),
            EnumScene.WIN: (self.win_scene, False),
            EnumScene.FINISH: (self.finish_scene, False),
            EnumScene.HIGHSCORE: (self.highscore_scene, False),
        }

        if self.state in scene_mapping:
            scene, hud = scene_mapping[self.state]
            self.current_scene = scene
            self.current_scene.enable()

            if hud:
                self.text_layout.enable()
                self.lives_layout.enable()

    def nextLevel(self) -> None:
        if self.no_level <= self.nb_level:
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
        self.highscores.addAndSave(
            game_score, self.highscore_filename_config)

    def infiniteLive(self) -> None:
        self.lives_layout.infiniteLive()

    def resetGame(self) -> None:
        self.levels = self._getLevels(self.levels_config)
        self.no_level = 0
        self.nb_level = len(self.levels) - 1

        self.current_score = 0

        # Additionnal Data
        self.death_malus = 100
        self.kill = 0
        self.is_lose = False
