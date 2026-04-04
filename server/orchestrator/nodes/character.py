from orchestrator.agents.character_agent import generate_characters


def character_node(state):
    characters = generate_characters(
        scene_data=state["scene_data"],
        constraints=state["constraints"],
        retry_feedback=state.get("character_error") or "",
        llm_client=state.get("llm_client"),
    )
    return {
        **state,
        "character_data": characters,
        "valid": False,
        "abort": False,
    }
