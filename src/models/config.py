from pathlib import Path
from typing import List

from pydantic import BaseModel, Field


class LevelValidation(BaseModel):
    """Validated dimensions for a single maze level.

    Attributes:
        width: Level grid width, in tiles (5-100).
        height: Level grid height, in tiles (5-100).
    """

    width: int = Field(gt=5, lt=26)
    height: int = Field(gt=5, lt=21)


class ConfigFileValidation(BaseModel):
    """Validated schema for the game's top-level configuration file.

    Attributes:
        highscore_filename: Path to the high-score JSON file.
        levels: Level configurations, at least 10 entries.
        lives: Starting lives per game.
        points_per_pacgum: Points per regular pac-gum.
        points_per_super_pacgum: Points per super pac-gum.
        points_per_ghost: Points per ghost eaten.
        seed: Maze generation seed.
        level_max_time: Time per level, in seconds.
    """

    highscore_filename: Path = Field(default=Path("config/highscores.json"))
    levels: List[LevelValidation] = Field(min_length=10)
    lives: int = Field(default=3, ge=1)
    points_per_pacgum: int = Field(default=10, ge=0)
    points_per_super_pacgum: int = Field(default=50, ge=0)
    points_per_ghost: int = Field(default=200, ge=0)
    seed: int
    level_max_time: int = Field(default=90, ge=1)
