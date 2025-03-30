from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.environment.variables import MONGO_CONNECTION_STRING, MONGO_DATABASE
from app.logging import log
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo_client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    app.state.db = app.state.mongo_client.get_database(MONGO_DATABASE)
    log.info(f"[DB] Connected to Mongo database: '{MONGO_DATABASE}' succesfully")
    yield
    app.state.mongo_client.close()
    log.info("[DB] Connection closed")
