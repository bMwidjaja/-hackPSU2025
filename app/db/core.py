from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient


async def lifespan(app: FastAPI):
    app.mongodb_client = AsyncIOMotorClient()
