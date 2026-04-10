from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

CURRENT_FILE = Path(__file__).resolve()
APP_ROOT = CURRENT_FILE.parents[3]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from config.db import get_db
from orchestrator.logger import get_logger
from image_gen.db.prompt_history_store import PromptHistoryStore
from services.engine import ImageGenerationService

logger = get_logger("services.workflows.editor")


class EditorWorkflowService:
    """Editor dashboard flow: orchestrator output -> shared image engine."""

    def __init__(self, image_service: ImageGenerationService | None = None):
        self.image_service = image_service or ImageGenerationService()
        self.prompt_history_store = PromptHistoryStore()

    def generate_from_orchestrator_output(
        self,
        orchestrator_output: Dict[str, Any],
        project_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        logger.info("Running editor workflow image generation")
        rendered_panels = self.image_service.generate_panels(orchestrator_output)
        final_output = orchestrator_output.get("final_output", {})
        if final_output:
            final_output["panels"] = self._attach_rendered_panels(
                panels=final_output.get("panels", []),
                rendered_panels=rendered_panels,
            )
            self._save_prompt_histories(final_output=final_output, rendered_panels=rendered_panels)

        package = {
            "final_output": final_output,
            "debug": orchestrator_output.get("debug", {}),
            "image_generation": rendered_panels,
            "orchestrator_output": orchestrator_output,
        }

        if project_id:
            self._persist_project(
                project_id=project_id,
                final_output=final_output,
                debug_data=package["debug"],
                image_generation=rendered_panels,
            )

        return package

    def _persist_project(
        self,
        project_id: str,
        final_output: Dict[str, Any],
        debug_data: Dict[str, Any],
        image_generation: List[Dict[str, Any]],
    ) -> None:
        db = get_db()
        db.projects.update_one(
            {"_id": project_id},
            {
                "$set": {
                    "panels": final_output.get("panels", []),
                    "characters": final_output.get("characters", []),
                    "debug": debug_data,
                    "image_generation": image_generation,
                }
            },
        )

    @staticmethod
    def _attach_rendered_panels(
        panels: List[Dict[str, Any]],
        rendered_panels: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        rendered_by_panel = {
            item["panel_id"]: item for item in rendered_panels if "panel_id" in item
        }
        merged: List[Dict[str, Any]] = []
        for panel in panels:
            panel_copy = dict(panel)
            render_result = rendered_by_panel.get(panel_copy.get("panel_id"))
            if render_result:
                panel_copy["image_generation"] = render_result
                panel_copy["image_path"] = render_result.get("output_path")
            merged.append(panel_copy)
        return merged

    def _save_prompt_histories(
        self,
        final_output: Dict[str, Any],
        rendered_panels: List[Dict[str, Any]],
    ) -> None:
        rendered_by_panel = {
            item["panel_id"]: item for item in rendered_panels if "panel_id" in item
        }
        for panel in final_output.get("panels", []):
            render_result = rendered_by_panel.get(panel.get("panel_id"))
            if not render_result:
                continue
            prompt = str(render_result.get("prompt", "")).strip()
            self.prompt_history_store.save_prompt_history(
                panel_id=int(panel["panel_id"]),
                prompt_data={
                    "original_prompt": prompt,
                    "final_render_prompt": prompt,
                    "character_anchor_tokens": self._extract_anchor_tokens(prompt),
                    "scene_metadata": self._build_scene_metadata(panel, final_output),
                    "last_model_used": render_result.get("model_used"),
                },
            )

    @staticmethod
    def _extract_anchor_tokens(prompt: str) -> List[str]:
        import re

        return re.findall(r"\[[A-Z0-9_]+]", prompt or "")

    @staticmethod
    def _build_scene_metadata(panel: Dict[str, Any], final_output: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "theme": panel.get("theme") or final_output.get("theme"),
            "scene_description": panel.get("scene_description"),
            "location": panel.get("location"),
            "time": panel.get("time"),
            "camera_angle": panel.get("camera_angle"),
            "action": panel.get("action"),
            "emotion": panel.get("emotion"),
            "characters": panel.get("characters", []),
            "dialogues": panel.get("dialogues", []),
        }
