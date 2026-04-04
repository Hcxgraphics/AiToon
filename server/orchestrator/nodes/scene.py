from orchestrator.agents.scene_agent import generate_scenes


def scene_node(state):
    scenes = generate_scenes(
        user_input=state["prompt"],
        constraints=state["constraints"],
        retry_feedback=state.get("scene_error") or "",
        llm_client=state.get("llm_client"),
    )
    return {
        **state,
        "scene_data": scenes,
        "valid": False,
        "abort": False,
    }
