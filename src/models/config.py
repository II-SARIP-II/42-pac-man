from pydantic import BaseModel, Field, ConfigDict
from typing import List
from pathlib import Path


class LevelValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: int = Field(gt=5, lt=100)
    height: int = Field(gt=5, lt=100)


class ConfigFileValidation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    highscore_filename: Path = Field(Path)
    levels: List[LevelValidation] = Field(default=[])
    lives: int = Field(default=3, ge=1)
    points_per_pacgum: int = Field(default=10, ge=0)
    points_per_super_pacgum: int = Field(default=50, ge=0)
    points_per_ghost: int = Field(default=200, ge=0)
    seed: int
    level_max_time: int = Field(default=90, ge=1)
