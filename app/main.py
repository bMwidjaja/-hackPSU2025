from fastapi import FastAPI
from app.routes import images, leaderboard
from app.environment.variables import MONGO_CONNECTION_STRING

app = FastAPI()

app.include_router(images.router)
app.include_router(leaderboard.router)


@app.get("/")
def root():
    return {"message": "api active"}
