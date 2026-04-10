from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from orchestrator.logger import get_logger
from services.workflows import EditorWorkflowService

router = APIRouter()
logger = get_logger("routes.editor")
editor_workflow_service = EditorWorkflowService()


class EditorGenerateRequest(BaseModel):
    project_id: Optional[str] = None
    orchestrator_output: Dict[str, Any]


@router.post("/editor/generate")
def generate_from_editor(data: EditorGenerateRequest):
    try:
        package = editor_workflow_service.generate_from_orchestrator_output(
            orchestrator_output=data.orchestrator_output,
            project_id=data.project_id,
        )
        return {
            "final_output": package["final_output"],
            "image_generation": package["image_generation"],
            "debug": package["debug"],
        }
    except Exception as exc:
        logger.error("Editor workflow generation failed: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail=str(exc))
