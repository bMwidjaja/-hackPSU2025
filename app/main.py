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
import llm
import base64

app = FastAPI()

# MongoDB connection
MONGODB_URL = "mongodb+srv://JunesPH:3koreankid45@hackpsu2025cluster.5qq8y0i.mongodb.net/hackpsu?retryWrites=true&w=majority"
client = motor_asyncio.AsyncIOMotorClient(MONGODB_URL)

# Get the collections from MongoDB
users_collection = client.hackpsu.users
images_collection = client.hackpsu.images
rating_collection = client.hackpsu.rating

# Create a directory to store uploaded images if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class User(BaseModel):
    name: str
    timestamp: datetime

class Image(BaseModel):
    user_id: str
    image_path: str
    timestamp: datetime

class Rating(BaseModel):
    user_id: str
    image_id: str
    score: int
    timestamp: datetime

    #This is to convert the datetime and ObjectId that's Python-specific to a JSON format
    class Config:
        json_encoders = {
            datetime: lambda x: x.isoformat(),
            ObjectId: lambda x: str(x)
        }

class ImageRequest(BaseModel):
    name: str
    image: str  # Base64 encoded image

@app.post("/submit-score/")
async def submit_score(request: Request):
    try:
        # Get JSON data from request
        data = await request.json()
        

        """
        # Validate request data
        if not data.get("name") or not data.get("image"):
            raise HTTPException(status_code=400, detail="Missing name or image data")
        """
        # For simplicity, always return score of 1
        score = 1
        
        # Save the image
        base64_image = data["image"]
        
        # Store rating data
        rating = Rating(user_id=user_id, image_id=image_id, score=score, timestamp=datetime.now())
        await rating_collection.insert_one(rating.model_dump())
        
        
        return {
            "message": "Score submitted successfully",
            "user_id": user_id,
            "image_id": image_id,
            "score": score,
            "name": data["name"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leaderboard/")
async def get_leaderboard():
    # Get all ratings sorted by score in descending order
    #The pipeline is to join the users collection with the ratings collection
    pipeline = [
        #Sort the ratings by score in descending order
        {"$sort": {"score": -1}},
        {   #Join both the users collection and the ratings collection
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }
        },
        {"$unwind": "$user"}
    ]
    
    cursor = rating_collection.aggregate(pipeline)
    entries = []
    async for entry in cursor:
        entry["_id"] = str(entry["_id"])
        entry["user_id"] = str(entry["user_id"])
        entry["user"]["_id"] = str(entry["user"]["_id"])
        entries.append(entry)
    return entries

@app.patch("/leaderboard/{rating_id}")
async def update_leaderboard_entry(rating_id: str, score: int):
    try:
        object_id = ObjectId(rating_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid rating ID")
    
    # Update the rating
    await rating_collection.update_one(
        {"_id": object_id},
        {"$set": {"score": score}}
    )
    
    # Get the updated entry
    updated_entry = await rating_collection.find_one({"_id": object_id})
    if not updated_entry:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    updated_entry["_id"] = str(updated_entry["_id"])
    updated_entry["user_id"] = str(updated_entry["user_id"])
    
    return {"message": "Rating updated successfully", "entry": updated_entry}

#Could create a new file to create the rate function

