from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class LeaderboardGet(BaseModel):
    pass


@router.get("/leaderboards")
def leaderboards_get():
    pass


class LeaderboardPost(BaseModel):
    pass


@router.post("/leaderboards")
def leaderboards_post():
    pass
