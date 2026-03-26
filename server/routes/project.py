from fastapi import APIRouter
from config.db import db

router = APIRouter()

@router.get("/project/{project_id}")
def get_project(project_id: str):
    project = db.projects.find_one({"project_id": project_id})

    if not project:
        return {"error": "Project not found"}

    project["_id"] = str(project["_id"])

    return project