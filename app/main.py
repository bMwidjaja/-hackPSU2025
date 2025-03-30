from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
from datetime import datetime
from pymongo import MongoClient
from motor import motor_asyncio
from bson import ObjectId
import json
import base64
from PIL import Image
import io
from llm import LLM  # Import the LLM class
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# MongoDB connection
MONGODB_URL = "mongodb+srv://JunesPH:3koreankid45@hackpsu2025cluster.5qq8y0i.mongodb.net/hackpsu?retryWrites=true&w=majority"
client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

# Get the collection from MongoDB
collection = client.hackpsu.scores

# Create a directory to store uploaded images if it doesn't exist
#Probably not needed
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#Probably not needed
class User(BaseModel): 
    name: str
    image: str
    timestamp: datetime

    #This is to convert the datetime and ObjectId that's Python-specific to a JSON format
    class Config:
        json_encoders = {
            datetime: lambda x: x.isoformat(),
            ObjectId: lambda x: str(x)
        }

#Probably not needed
class ImageRequest(BaseModel):
    name: str
    image: str  # Base64 encoded image

class ScoreEntry(BaseModel):
    name: str
    image: str  # Base64 encoded image
    score: int
    timestamp: datetime

    class Config:
        json_encoders = {
            datetime: lambda x: x.isoformat(),
            ObjectId: lambda x: str(x)
        }

@app.post("/submit-score/")
async def submit_score(request: Request):
    try:
        # Get JSON data from request
        data = await request.json()
        
        # Validate request data
        if not data.get("name") or not data.get("image"):
            raise HTTPException(status_code=400, detail="Missing name or image data")
        
        # Process image with LLM
        llm = LLM()  # Create an instance of the LLM class
        score = llm.rate_pic(data["image"])  # Get the score from LLM
        
        # Create document to insert
        document = {
            "name": data["name"],
            "image": data["image"],
            "score": score,
            "timestamp": datetime.now()
        }
        
        # Insert the document
        result = await collection.insert_one(document)
        
        # Return response with score and other data
        return {
            "status": "success",
            "score": score,
            "name": data["name"],
            "message": "Score submitted successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Hopefully this works
@app.get("/leaderboard/")
async def get_leaderboard():
    # Get all scores sorted by score in descending order
    pipeline = [
        {"$sort": {"score": -1}}  # -1 for descending order (highest first)
    ]
    
    cursor = collection.aggregate(pipeline)
    entries = []
    async for entry in cursor:
        entry["_id"] = str(entry["_id"])  # Convert ObjectId to string for JSON
        entries.append(entry)
    return entries

#Hopefully this works
@app.patch("/leaderboard/{rating_id}")
async def update_leaderboard_entry(rating_id: str, score: int):
    try:
        object_id = ObjectId(rating_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid rating ID")
    
    # Update the rating
    await collection.update_one(
        {"_id": object_id},
        {"$set": {"score": score}}
    )
    
    # Get the updated entry
    updated_entry = await collection.find_one({"_id": object_id})
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    updated_entry["_id"] = str(updated_entry["_id"])
    
    return {"message": "Entry updated successfully", 
            "entry": updated_entry}

#Could create a new file to create the rate function

