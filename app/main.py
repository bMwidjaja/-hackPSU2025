from fastapi import FastAPI
from app.db.core import lifespan
from app.routes import images, leaderboard

app = FastAPI(lifespan=lifespan)

app.include_router(images.router)
app.include_router(leaderboard.router)


@app.get("/")
def root():
    return {"message": "api active"}
