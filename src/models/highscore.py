from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import json
from src.utils_io import write_json_file, load_json_file

class Score(BaseModel):
    name: str = Field(min_length=1, max_length=10, pattern=r"^[a-zA-Z0-9 ]+$")
    score: int = Field(default=0)
    date: datetime


class ScoresList(BaseModel):
    scores: List[Score] = Field(default=[], max_length=10)

    def addAndSave(self, game_score: Score, filename: str) -> None:
        self.scores.append(game_score)

        self.scores = sorted(
            self.scores,
            key=lambda x: x.score,
            reverse=True
        )[:10]

        clean_highscores = json.loads(self.model_dump_json())
        write_json_file(clean_highscores, filename)

    @classmethod
    def from_json(cls, filename: str) -> "ScoresList":
        try:
            return ScoresList(**load_json_file(filename))
        except (ValueError, FileNotFoundError):
            print(f"{filename} was empty or invalid.")
            return ScoresList(scores=[])
