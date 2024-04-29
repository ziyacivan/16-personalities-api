from typing import List
from pydantic import BaseModel


class AnswerItem(BaseModel):
    text: str
    answer: int

class Answer(BaseModel):
    gender: str
    data: List[AnswerItem]