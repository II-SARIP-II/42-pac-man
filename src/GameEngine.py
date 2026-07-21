from datetime import datetime
from typing import List

from ursina import camera, destroy
from sys import exit

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
    """Central controller for scenes, level progression, and game state."""

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
        """Initialize the engine from configuration and set up the game.

        Args:
            highscore_filename (str): Path to the high-score JSON file.
            levels (List[LevelValidation]): Level configurations.
            lives (int): Starting lives per game.
            points_per_pacgum (int): Points per regular pac-gum.
            points_per_super_pacgum (int): Points per super pac-gum.
            points_per_ghost (int): Points per ghost eaten.
            seed (int): Maze generation seed.
            level_max_time (int): Time per level, in seconds.

        Returns:
            None.
        """
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

        self.level_generator = LevelGenerator(self.seed)

        self.resetGameData()
        self._setupScenes()

    def resetGameData(self) -> None:
        """Create a fresh `GameData` using the engine's configuration.

        Returns:
            None.
        """
        self.game_data = GameData(
            total_lives=self.lives,
            total_time=self.level_max_time,
            points_per_pacgum=self.points_per_pacgum,
            points_per_super_pacgum=self.points_per_super_pacgum,
            points_per_ghost=self.points_per_ghost,
            seed=self.seed
        )

    def initLevel(self) -> None:
        """Reset level progression to the first configured level.

        Returns:
            None.
        """
        self.no_level = 0
        self.nb_level = len(self.levels_config) - 1

    def _setupScenes(self) -> None:
        """Instantiate every non-gameplay scene and set the initial scene.

        Returns:
            None.
        """
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
        """Generate a new level and create its `GameScene`.

        Returns:
            None.
        """
        if self.game_scene:
            self.game_scene.cleanUp()
            destroy(self.game_scene)

        self.level = self.getLevel()
        self.game_scene = GameScene(
            game_engine=self,
            level=self.level,
            game_data=self.game_data
        )

        self.game_scene.disable()

    def getLevel(self) -> Level:
        """Generate the `Level` for the current level index.

        Returns:
            Level: The newly generated level.
        """
        return self.level_generator.generateLevel(
            self.levels_config[self.no_level]
            )

    def quitGame(self) -> None:
        """Quit the application.

        Returns:
            None.
        """
        exit()

    def changeScene(self, new_scene: Scene) -> None:
        """Switch the active scene, calling exit/entry lifecycle hooks.

        Args:
            new_scene (Scene): Scene to switch to.

        Returns:
            None.
        """
        self.current_scene.onExit()
        self.prev_scene = self.current_scene
        self.current_scene = new_scene
        self.current_scene.onEntry()

    def nextLevel(self) -> None:
        """Advance to the next level, or finish the game if none remain.

        Returns:
            None.
        """
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
        """Award the player points for eating a regular pac-gum.

        Returns:
            None.
        """
        self.game_data.addScore(self.game_data.points_per_pacgum_config)

    def eatSuperPacgum(self) -> None:
        """Award the player points for eating a super pac-gum.

        Returns:
            None.
        """
        self.game_data.addScore(self.game_data.points_per_super_pacgum_config)

    def eatGhost(self) -> None:
        """Award the player points and a kill credit for eating a ghost.

        Returns:
            None.
        """
        self.game_data.addScore(self.game_data.points_per_ghost_config)
        self.game_data.addKill(1)

    def submitScore(self, name: str) -> None:
        """Save the current score under the given name and return to the menu.

        Args:
            name (str): Player's chosen leaderboard name.

        Returns:
            None.
        """
        name = name.strip()
        if not name:
            print("The name cannot be empty.")
            return

        self.writeHighscore(name)

        self.highscores = ScoresList.loadFromJson(
            self.highscore_filename_config)

        self.changeScene(self.menu_scene)

    def writeHighscore(self, name: str) -> None:
        """Build and persist a new high-score entry for the given name.

        Args:
            name (str): Player's chosen leaderboard name.

        Returns:
            None.
        """
        game_score = Score(
            name=name,
            score=self.game_data.score,
            date=datetime.now()
            )

        self.highscores.addAndSave(
            game_score, self.highscore_filename_config)
