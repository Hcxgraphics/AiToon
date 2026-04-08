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

        for panel in parsed:
            for char in panel.get("characters", []):

                if not char.get("appearance") or not char["appearance"].strip():
                    char["appearance"] = "Generic character with distinct look"

                if not char.get("emotion") or not char["emotion"].strip():
                    char["emotion"] = "Neutral"

                if not char.get("pose") or not char["pose"].strip():
                    char["pose"] = "Standing"

                if not char.get("name") or not char["name"].strip():
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

