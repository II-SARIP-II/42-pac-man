from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class Score(BaseModel):
    name: str = Field(min_length=1, max_length=10, pattern=r"^[a-zA-Z0-9 ]+$")
    score: int = Field(ge=0)
    date: datetime


class ScoresList(BaseModel):
    scores: List[Score] = Field(default=[], max_length=10)
