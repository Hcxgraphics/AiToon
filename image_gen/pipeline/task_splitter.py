from __future__ import annotations

from typing import Any, Dict, List

from image_gen.core.contracts import SceneTask


class SceneTaskSplitter:
    """Converts orchestrator output into independent scene render tasks."""

    def split(self, payload: Dict[str, Any]) -> List[SceneTask]:
        if not isinstance(payload, dict):
            raise TypeError(f"Expected payload to be a dict, got {type(payload).__name__}")

        final_output = payload.get("final_output", payload)
        if not isinstance(final_output, dict):
            raise TypeError(
                f"Expected payload['final_output'] to be a dict, got {type(final_output).__name__}"
            )

        panels = final_output.get("panels", [])
        if not isinstance(panels, list):
            raise TypeError(f"Expected panels to be a list, got {type(panels).__name__}")

        characters = final_output.get("characters", [])
        character_map = {
            str(character.get("char_id")): character
            for character in characters
            if isinstance(character, dict) and character.get("char_id")
        }
        default_theme = final_output.get("theme")
        story_summary = str(final_output.get("story_summary", "")).strip()

        return [
            SceneTask.from_panel(
                panel,
                default_theme=default_theme,
                payload_characters=character_map,
                story_summary=story_summary,
            )
            for panel in panels
        ]
