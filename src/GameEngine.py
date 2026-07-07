from typing import List

from ursina import camera, destroy

from src.core.Level import Level
from src.core.LevelGenerator import LevelGenerator
from src.models.config import LevelValidation
from src.models.highscore import ScoresList, Score
from src.scene.Scene import Scene
from src.scene.GameScene import GameScene
from src.scene.LoseScene import LoseScene
from src.scene.MenuScene import MenuScene
from src.scene.PauseScene import PauseScene
from src.scene.WinScene import WinScene
from src.scene.FinishScene import FinishScene
from src.scene.LeaderboardScene import LeaderboardScene
from src.utils_io import load_json_file, write_json_file
import json
from datetime import datetime
from src.GameData import GameData


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

        self.levels: List[Level] = self._getLevels(self.levels_config)
        self.no_level = 0
        self.nb_level = len(self.levels) - 1

        self.lives = lives
        self.level_max_time = level_max_time
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost
        self.seed = seed

        self.highscores = self._getScores(self.highscore_filename_config)

        camera.position = (0, 50, 0)
        camera.rotation = (90, 0, 0)

        self.resetGame()
        self._setupScenes()

    def resetGame(self) -> None:
        self.game_data = GameData(
            total_lives=self.lives,
            total_time=self.level_max_time,
            points_per_pacgum=self.points_per_pacgum,
            points_per_super_pacgum=self.points_per_super_pacgum,
            points_per_ghost=self.points_per_ghost,
            seed=self.seed
        )

        self.levels = self._getLevels(self.levels_config)
        self.no_level = 0
        self.nb_level = len(self.levels) - 1

    def _setupScenes(self) -> None:
        self.game_scene = None

        self.pause_scene = PauseScene(self)
        self.pause_scene.disable()

        self.finish_scene = FinishScene(self)
        self.finish_scene.disable()

        self.leaderboard_scene = LeaderboardScene(self, self.highscores)
        self.leaderboard_scene.disable()

        self.win_scene = WinScene(self, self.game_data)
        self.win_scene.disable()

        self.lose_scene = LoseScene(self, self.game_data)
        self.lose_scene.disable()

        self.menu_scene = MenuScene(self)

        self.current_scene = self.menu_scene

    def newGameScene(self) -> None:
        if self.game_scene:
            self.game_scene.cleanUp()
            destroy(self.game_scene)

        self.game_scene = GameScene(
            game_engine=self,
            level=self.levels[self.no_level],
            game_data=self.game_data
        )

        self.game_scene.disable()

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

    def changeScene(self, new_scene: Scene) -> None:
        self.current_scene.onExit()
        self.current_scene = new_scene
        self.current_scene.onEntry()

    def nextLevel(self) -> None:
        if self.no_level <= self.nb_level:
            self.newGameScene()
            self.changeScene(self.game_scene)

        else:
            self.changeScene(self.finish_scene)

    def eatPacgum(self) -> None:
        self.game_data.addScore(self.game_data.points_per_pacgum_config)

    def eatSuperPacgum(self) -> None:
        self.game_data.addScore(self.game_data.points_per_super_pacgum_config)

    def eatGhost(self) -> None:
        self.game_data.addScore(self.game_data.points_per_ghost_config)
        self.game_data.addKill(1)

    def submitScore(self) -> None:
        name = self.finish_scene.player_name.text.strip()
        if not name:
            print("The name cannot be empty.")
            return

        self.write_highscore(name)
        self.changeScene(self.menu_scene)

    def write_highscore(self, name: str) -> None:
        game_score = Score(
            name=name,
            score=self.game_data.score,
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
