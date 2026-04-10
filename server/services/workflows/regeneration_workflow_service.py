from __future__ import annotations

from typing import Any, Dict, Optional

from config.db import get_db
from orchestrator.logger import get_logger
from services.engine import ImageGenerationService

logger = get_logger("services.workflows.regeneration")


class RegenerationWorkflowService:
    """Dashboard regeneration flow for panel inpainting and targeted updates."""

    def __init__(self, image_service: ImageGenerationService | None = None):
        self.image_service = image_service or ImageGenerationService()

    def regenerate_panel(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        panel_id = int(payload["panel_id"])
        prompt = str(payload["prompt"]).strip()
        image_url = payload.get("image_url")
        mask_url = payload.get("mask_url")
        project_id: Optional[str] = payload.get("project_id")

        logger.info("Running regeneration workflow for panel=%s", panel_id)
        result = self.image_service.regenerate_panel(
            panel_id=panel_id,
            prompt=prompt,
            image_url=image_url,
            mask_url=mask_url,
        )

        if project_id:
            self._persist_regeneration(project_id=project_id, regeneration=result)

        return {
            "panel_id": panel_id,
            "image_generation": result,
        }

    @staticmethod
    def _persist_regeneration(project_id: str, regeneration: Dict[str, Any]) -> None:
        db = get_db()
        db.projects.update_one(
            {"_id": project_id},
            {
                "$set": {
                    "last_regeneration": regeneration,
                }
            },
        )
