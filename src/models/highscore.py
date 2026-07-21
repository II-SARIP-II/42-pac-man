import json
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

from src.utils_io import load_json_file, write_json_file


class Score(BaseModel):
    """A single leaderboard entry.

    Attributes:
        name: Player's name (1-10 alphanumeric characters/spaces).
        score: Points achieved.
        date: When the score was recorded.
    """

    name: str = Field(min_length=1, max_length=10, pattern=r"^[a-zA-Z0-9 ]+$")
    score: int = Field(default=0)
    date: datetime


class ScoresList(BaseModel):
    """A persisted, ranked list of the top high scores.

    Attributes:
        scores: The stored high scores, capped at 10 entries.
    """

    scores: List[Score] = Field(default=[], max_length=10)

    def addAndSave(self, game_score: Score, filename: str) -> None:
        """Add a new score, keep only the top 10, and persist to disk.

        Args:
            game_score (Score): Score entry to add.
            filename (str): Intended output path (unused).

        Returns:
            None.
        """
        self.scores.append(game_score)
        self.scores = sorted(
            self.scores,
            key=lambda x: x.score,
            reverse=True
            )[:10]

        clean_dict = json.loads(self.model_dump_json())
        write_json_file(clean_dict, filename)

    @classmethod
    def loadFromJson(cls, filename: str) -> "ScoresList":
        """Load a `ScoresList` from a JSON file.

        Args:
            filename (str): Path of the JSON file.

        Returns:
            ScoresList: The loaded scores, or empty if unreadable.
        """
        try:
            return cls(**load_json_file(filename))
        except (ValueError, FileNotFoundError):
            print(f"{filename} was empty or invalid.")
            return cls(scores=[])
