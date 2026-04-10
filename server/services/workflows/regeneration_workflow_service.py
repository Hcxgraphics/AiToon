from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, Optional

CURRENT_FILE = Path(__file__).resolve()
APP_ROOT = CURRENT_FILE.parents[3]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from config.db import get_db
from image_gen.db.prompt_history_store import PromptHistoryStore
from orchestrator.logger import get_logger
from services.engine import ImageGenerationService
from services.workflows.prompt_regeneration_service import PromptRegenerationService

logger = get_logger("services.workflows.regeneration")


class RegenerationWorkflowService:
    """Dashboard regeneration flow using the same active generation models."""

    def __init__(self, image_service: ImageGenerationService | None = None):
        self.image_service = image_service or ImageGenerationService()
        self.prompt_history_store = PromptHistoryStore()
        self.prompt_regeneration_service = PromptRegenerationService(
            prompt_history_store=self.prompt_history_store
        )

    def regenerate_panel(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        panel_id = int(payload["panel_id"])
        regeneration_instruction = str(payload["prompt"]).strip()
        project_id: Optional[str] = payload.get("project_id")
        prompt_history = self.prompt_history_store.fetch_prompt_history(panel_id)
        preferred_model = payload.get("model_used") or self._resolve_previous_model(
            panel_id=panel_id,
            project_id=project_id,
        )
        fused_prompt = self.prompt_regeneration_service.build_regeneration_prompt(
            panel_id=panel_id,
            regeneration_instruction=regeneration_instruction,
        )

        logger.info("Running regeneration workflow for panel=%s", panel_id)
        result = self.image_service.regenerate_panel(
            panel_id=panel_id,
            prompt=fused_prompt,
            preferred_model=preferred_model,
        )
        self.prompt_history_store.save_prompt_history(
            panel_id=panel_id,
            prompt_data={
                "original_prompt": (prompt_history or {}).get("original_prompt") or fused_prompt,
                "final_render_prompt": fused_prompt,
                "character_anchor_tokens": (prompt_history or {}).get("character_anchor_tokens", []),
                "scene_metadata": (prompt_history or {}).get("scene_metadata", {}),
                "last_model_used": result.get("model_used"),
                "latest_regeneration_instruction": regeneration_instruction,
            },
        )

        if project_id:
            self._persist_regeneration(project_id=project_id, regeneration=result)

        return {
            "panel_id": panel_id,
            "fused_prompt": fused_prompt,
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

    @staticmethod
    def _resolve_previous_model(panel_id: int, project_id: Optional[str]) -> Optional[str]:
        if not project_id:
            return None

        db = get_db()
        project = db.projects.find_one({"_id": project_id}, {"panels": 1, "image_generation": 1})
        if not project:
            return None

        for panel in project.get("panels", []):
            if panel.get("panel_id") == panel_id:
                image_generation = panel.get("image_generation")
                if isinstance(image_generation, dict) and image_generation.get("model_used"):
                    return image_generation["model_used"]

        for item in project.get("image_generation", []):
            if item.get("panel_id") == panel_id and item.get("model_used"):
                return item["model_used"]

        return None
