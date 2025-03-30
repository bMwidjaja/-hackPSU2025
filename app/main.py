from fastapi import Form, FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
from datetime import datetime

app = FastAPI()

# Create a directory to store uploaded images if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class LeaderboardEntry(BaseModel):
    name: str
    score: int
    image_path: str
    timestamp: datetime

class LeaderboardUpdate(BaseModel):
    name: Optional[str] = None
    score: Optional[int] = None
    image_path: Optional[str] = None

# In-memory storage for leaderboard entries
leaderboard_entries: List[LeaderboardEntry] = []

@app.post("/submit-score/")
async def submit_score(
    name: str = Form(...),
    image: UploadFile = File(...)
):
    # Save the uploaded image
    #os.path.join to create a full path to the image
    #the f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg" ensures uniqueness
    
    image_path = os.path.join(UPLOAD_DIR, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    #with open to open the image file in binary write mode (wb) 
    #must be written as a binary file to prevent corruption
    #buffer is a temporary storage for the image data
    with open(image_path, "wb") as buffer:
        #copyfileobj to copy the image data from the uploaded file to the opened file (buffer)
        shutil.copyfileobj(image.file, buffer)
    
    #Get score from LLM
    score = 0  # This should be replaced with the LLM's score
    
    # Create new leaderboard entry
    entry = LeaderboardEntry(
        name=name,
        score=score,
        image_path=image_path,
        timestamp=datetime.now()
    )
    
    # Add to leaderboard
    leaderboard_entries.append(entry)
    
    # Sort leaderboard by score (highest first)
    leaderboard_entries.sort(key=lambda x: x.score, reverse=True)
    
    return {"message": "Score submitted successfully", "entry": entry}

@app.get("/leaderboard/")
def get_leaderboard():
    return leaderboard_entries

@app.patch("/leaderboard/{entry_index}")
async def update_leaderboard_entry(entry_index: int, update: LeaderboardUpdate):
    if entry_index < 0 or entry_index >= len(leaderboard_entries):
        raise HTTPException(status_code=404, detail="Entry not found")
    
    entry = leaderboard_entries[entry_index]
    
    # Update only the provided fields
    if update.name is not None:
        entry.name = update.name
    if update.score is not None:
        entry.score = update.score
    if update.image_path is not None:
        entry.image_path = update.image_path
    
    # Re-sort the leaderboard
    leaderboard_entries.sort(key=lambda x: x.score, reverse=True)
    
    return {"message": "Entry updated successfully", "entry": entry}

