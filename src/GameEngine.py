from datetime import datetime
from typing import List

from ursina import camera, destroy

from src.core.Level import Level
from src.core.LevelGenerator import LevelGenerator
from src.GameData import GameData
from src.models.config import LevelValidation
from src.models.highscore import Score, ScoresList
from src.scene.FinishScene import FinishScene
from src.scene.GameScene import GameScene
from src.scene.LeaderboardScene import LeaderboardScene
from src.scene.LoseScene import LoseScene
from src.scene.MenuScene import MenuScene
from src.scene.PauseScene import PauseScene
from src.scene.InstructionScene import InstructionScene
from src.scene.Scene import Scene
from src.scene.WinScene import WinScene


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

        self.lives = lives
        self.level_max_time = level_max_time
        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = points_per_super_pacgum
        self.points_per_ghost = points_per_ghost
        self.seed = seed

        self.highscores = ScoresList.loadFromJson(
            self.highscore_filename_config)

        camera.position = (0, 55, 0)
        camera.rotation = (90, 0, 0)

        self.resetGameData()
        self._setupScenes()

    def resetGameData(self) -> None:
        self.game_data = GameData(
            total_lives=self.lives,
            total_time=self.level_max_time,
            points_per_pacgum=self.points_per_pacgum,
            points_per_super_pacgum=self.points_per_super_pacgum,
            points_per_ghost=self.points_per_ghost,
            seed=self.seed
        )

        self.levels = self.getLevels()
        self.no_level = 0
        self.nb_level = len(self.levels) - 1

    def _setupScenes(self) -> None:
        self.game_scene: None | GameScene = None

        self.pause_scene = PauseScene(self)
        self.pause_scene.disable()

        self.finish_scene = FinishScene(self)
        self.finish_scene.disable()

        self.leaderboard_scene = LeaderboardScene(self)
        self.leaderboard_scene.disable()

        self.win_scene = WinScene(self)
        self.win_scene.disable()

        self.lose_scene = LoseScene(self)
        self.lose_scene.disable()

        self.instruction_scene = InstructionScene(self)
        self.instruction_scene.disable()

        self.menu_scene = MenuScene(self)

        self.current_scene = self.menu_scene
        self.prev_scene = self.current_scene

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

    def getLevels(self) -> List[Level]:
        level_generator = LevelGenerator(self.seed)
        levels: List[Level] = []

        for level in self.levels_config:
            levels.append(level_generator.generateLevel(level))
        return levels

    def quitGame(self) -> None:
        quit()

    def changeScene(self, new_scene: Scene) -> None:
        self.current_scene.onExit()
        self.prev_scene = self.current_scene
        self.current_scene = new_scene
        self.current_scene.onEntry()

    def nextLevel(self) -> None:
        self.no_level += 1
        if self.no_level <= self.nb_level:
            if self.game_data.toggle_infinite_lives:
                self.game_data.infiniteLives()
            self.newGameScene()
            if self.game_scene:
                self.game_data.addLevel()
                self.game_data.resetTimer()
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

    def submitScore(self, name: str) -> None:
        name = name.strip()
        if not name:
            print("The name cannot be empty.")
            return

        self.writeHighscore(name)

        self.highscores = ScoresList.loadFromJson(
            self.highscore_filename_config)

        self.changeScene(self.menu_scene)

    def writeHighscore(self, name: str) -> None:
        game_score = Score(
            name=name,
            score=self.game_data.score,
            date=datetime.now()
            )

        self.highscores.addAndSave(
            game_score, self.highscore_filename_config)
