from typing import Any, Dict, List

from orchestrator.agents.llm import llm
from orchestrator.agents.utils import load_prompt, parse_json_response, render_json

def generate_dialogues(
    scene_data,
    character_data,
    constraints: Dict[str, List[str]],
    retry_feedback: str = "",
    llm_client: Any = None,
):
    prompt = load_prompt("dialogue_prompt.txt").format(
        bubble_types=render_json(constraints.get("bubble_types", [])),
        scene_data=render_json(scene_data),
        character_data=render_json(character_data),
        retry_feedback=retry_feedback or "None",
    )
    raw = (llm_client or llm).generate(prompt, task_type="fast_agent")

    try:
        parsed = parse_json_response(raw)
    except ValueError as exc:
        return {"error": f"invalid_json: {exc}", "raw": raw}

    if not isinstance(parsed, list):
        return {"error": "dialogue_output_must_be_a_list", "raw": raw}

    return parsed
