from orchestrator.agents.dialogue_agent import generate_dialogues


def dialogue_node(state):
    dialogues = generate_dialogues(
        scene_data=state["scene_data"],
        character_data=state["character_data"],
        constraints=state["constraints"],
        retry_feedback=state.get("dialogue_error") or "",
        llm_client=state.get("llm_client"),
    )
    return {
        **state,
        "dialogue_data": dialogues,
        "valid": False,
        "abort": False,
    }
