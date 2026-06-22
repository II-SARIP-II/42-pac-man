from pydantic import BaseModel, Field, FilePath
from typing import List
from datetime import datetime


class Score(BaseModel):
    name: str = Field(min_length=1, max_length=40)
    score: int = Field(default=0)
    date: datetime


class ScoresList(BaseModel):
    scores: List[Score] = Field(default=[])
