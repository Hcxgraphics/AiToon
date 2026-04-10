from __future__ import annotations

from typing import Any, Dict, List, Optional

from config.db import get_db
from orchestrator.core.graph import run_pipeline
from orchestrator.logger import get_logger
from services.engine import ImageGenerationService

DEFAULT_BUBBLE_TYPES = [
    "Speech: oval",
    "Speech: rectangle",
    "Thought (Cloud like)",
    "Whisper (Dashed or faint outline)",
    "Shout(Jagged / spiky)",
    "Robot Electronic (Zigzag or geometric)",
]

logger = get_logger("services.workflows.starter")


class StarterWorkflowService:
    """Starter comic flow: prompt input -> orchestrator -> shared image engine."""

    def __init__(self, image_service: ImageGenerationService | None = None):
        self.image_service = image_service or ImageGenerationService()

    def generate_starter_comic(
        self,
        project_id: str,
        storyline: str,
        summary: str = "",
        characters: Optional[List[dict]] = None,
        theme: Optional[str] = None,
        user_id: str = "test_user",
    ) -> Dict[str, Any]:
        orchestrator_result = self.run_orchestrator(
            prompt=self._build_story_prompt(storyline=storyline, summary=summary, characters=characters or []),
            theme=theme,
            user_id=user_id,
        )
        package = self._build_generation_package(orchestrator_result)
        self._persist_project(
            project_id=project_id,
            final_output=package["final_output"],
            debug_data=package["debug"],
            image_generation=package["image_generation"],
        )
        return package

    def create_package_from_prompt(
        self,
        prompt: str,
        theme: Optional[str],
        user_id: str = "test_user",
    ) -> Dict[str, Any]:
        orchestrator_result = self.run_orchestrator(prompt=prompt, theme=theme, user_id=user_id)
        return self._build_generation_package(orchestrator_result)

    def run_orchestrator(self, prompt: str, theme: Optional[str], user_id: str = "test_user") -> Dict[str, Any]:
        selected_theme = theme or "Anime"
        logger.info("Running starter workflow orchestrator for theme=%s", selected_theme)

        def constraints_provider() -> Dict[str, List[str]]:
            return {
                "themes": [selected_theme],
                "bubble_types": DEFAULT_BUBBLE_TYPES,
            }

        return run_pipeline(
            user_input=prompt,
            constraints_provider=constraints_provider,
            user_id=user_id,
        )

    def _build_generation_package(self, orchestrator_result: Dict[str, Any]) -> Dict[str, Any]:
        rendered_panels = self.image_service.generate_panels(orchestrator_result)
        final_output = orchestrator_result.get("final_output", {})
        if final_output:
            final_output["panels"] = self._attach_rendered_panels(
                panels=final_output.get("panels", []),
                rendered_panels=rendered_panels,
            )
        return {
            "final_output": final_output,
            "debug": orchestrator_result.get("debug", {}),
            "image_generation": rendered_panels,
            "orchestrator_result": orchestrator_result,
        }

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
    def _build_story_prompt(storyline: str, summary: str, characters: List[dict]) -> str:
        prompt_lines = [
            f"Storyline: {storyline}",
            f"Summary: {summary}",
        ]
        if characters:
            prompt_lines.append("Characters:")
            for character in characters:
                prompt_lines.append(
                    (
                        f"- Name: {character.get('name', 'Unknown')}; "
                        f"Appearance: {character.get('appearance', '')}; "
                        f"Style: {character.get('style', '')}; "
                        f"Personality: {character.get('personality', '')}"
                    ).strip()
                )
        return "\n".join(prompt_lines)

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
