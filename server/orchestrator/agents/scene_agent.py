from typing import Any, Dict, List

from orchestrator.agents.llm import llm
from orchestrator.agents.utils import load_prompt, parse_json_response, render_json


def generate_scenes(
    user_input: str,
    constraints: Dict[str, List[str]],
    retry_feedback: str = "",
    llm_client: Any = None,
):
    prompt = load_prompt("scene_prompt.txt").format(
        user_input=user_input,
        themes=render_json(constraints.get("themes", [])),
        retry_feedback=retry_feedback or "None",
    )
    raw = (llm_client or llm).generate(prompt, task_type="long_story")

    print("\nRAW SCENE OUTPUT:\n" , raw)

    try:
        parsed = parse_json_response(raw)

        if isinstance(parsed, dict) and "panels" in parsed:
            parsed = parsed["panels"]
            
    except ValueError as exc:
        return {"error": f"invalid_json: {exc}", "raw": raw}

    if not isinstance(parsed, list):
        return {"error": "scene_output_must_be_a_list", "raw": raw}

    return parsed
