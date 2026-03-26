from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from config.db import db
import uuid

router = APIRouter()

class SetupRequest(BaseModel):
    theme: str
    characters: list
    storyline: str 
    tagline: Optional[str] = None
    summary: Optional[str] = None

@router.post("/setup")
def create_project(data: SetupRequest):
    project_id = str(uuid.uuid4())

    project = {
        "project_id": project_id,
        "theme": data.theme,
        "characters": data.characters,
        "story": {
            "storyline": data.storyline,
            "tagline": data.tagline,
            "summary": data.summary
        },
        "panels": [],  # empty for now
    }

    db.projects.insert_one(project)

    return {
        "project_id": project_id,
        "message": "Project created successfully"
    }