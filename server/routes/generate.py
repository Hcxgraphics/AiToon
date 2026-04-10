from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from orchestrator.logger import get_logger
from services.workflows import StarterWorkflowService

router = APIRouter()
logger = get_logger("routes.generate")
starter_workflow_service = StarterWorkflowService()


class StarterGenerateRequest(BaseModel):
    project_id: str
    storyline: str
    summary: Optional[str] = ""
    characters: Optional[List[dict]] = []
    theme: Optional[str] = None
    user_id: Optional[str] = "test_user"


@router.post("/generate")
def generate(data: StarterGenerateRequest):
    try:
        package = starter_workflow_service.generate_starter_comic(
            project_id=data.project_id,
            storyline=data.storyline,
            summary=data.summary or "",
            characters=data.characters or [],
            theme=data.theme,
            user_id=data.user_id or "test_user",
        )
        return {
            "final_output": package["final_output"],
            "image_generation": package["image_generation"],
            "debug": package["debug"],
        }
    except Exception as exc:
        logger.error("Starter workflow generation failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
