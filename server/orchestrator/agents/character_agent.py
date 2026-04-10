from typing import Any, Dict, List

from orchestrator.agents.llm import llm
from orchestrator.agents.utils import load_prompt, parse_json_response, render_json


def generate_characters(
    scene_data,
    constraints: Dict[str, List[str]],
    retry_feedback: str = "",
    llm_client: Any = None,
):
    prompt = load_prompt("character_prompt.txt").format(
        scene_data=render_json(scene_data),
        themes=render_json(constraints.get("themes", [])),
        retry_feedback=retry_feedback or "None",
    )
    raw = (llm_client or llm).generate(prompt, task_type="fast_agent")

    try:
        parsed = parse_json_response(raw)

        normalized = []

        for panel in parsed:
            if not isinstance(panel, dict):
                continue

            if "characters" not in panel or not isinstance(panel["characters"], list):
                panel["characters"] = []

            for char in panel["characters"]:
                if not isinstance(char, dict):
                    continue

                if not char.get("appearance"):
                    char["appearance"] = "Generic character with distinct look"

                if not char.get("emotion"):
                    char["emotion"] = "Neutral"

                if not char.get("pose"):
                    char["pose"] = "Standing"

                if not char.get("name"):
                    char["name"] = "Unknown"

    except ValueError as exc:
        return {"error": f"invalid_json: {exc}", "raw": raw}

    if not isinstance(parsed, list):
        return [
        {
            "panel_id": panel.get("panel_id"),
            "characters": [
                {
                    "char_id": "c1",
                    "name": "Unknown",
                    "appearance": "Default",
                    "emotion": "Neutral",
                    "pose": "Standing"
                }
            ]
        }
        for panel in scene_data
    ]

    return parsed

