from __future__ import annotations

from typing import Any, Dict, List, Optional

from config.db import get_db
from orchestrator.logger import get_logger
from services.engine import ImageGenerationService

logger = get_logger("services.workflows.editor")


class EditorWorkflowService:
    """Editor dashboard flow: orchestrator output -> shared image engine."""

    def __init__(self, image_service: ImageGenerationService | None = None):
        self.image_service = image_service or ImageGenerationService()

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
