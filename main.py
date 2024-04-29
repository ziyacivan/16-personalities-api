from typing import List
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from constants import QUESTIONS
from clients import PersonalitiesClient
from models import Answer

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["localhost"]
)

@app.get("/questions")
def questions(limit: int = 10):
    return QUESTIONS[:limit]

@app.post("/send-answers")
def send_answers(answer: Answer):
    gender = answer.gender
    answers = jsonable_encoder(answer.data)
    result = PersonalitiesClient().send_answers(answers, gender)
    return result