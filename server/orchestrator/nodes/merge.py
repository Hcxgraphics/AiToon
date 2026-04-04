from orchestrator.schema.validator import validate_master


def merge_node(state):
    scene_data = state.get("scene_data", [])
    character_data = state.get("character_data", [])
    dialogue_data = state.get("dialogue_data", [])

    characters_by_id = {}
    character_ids_by_panel = {}
    for panel in character_data:
        if not isinstance(panel, dict):
            continue
        panel_id = panel.get("panel_id")
        panel_char_ids = []
        for character in panel.get("characters", []):
            if not isinstance(character, dict):
                continue
            char_id = character.get("char_id")
            if not char_id:
                continue
            characters_by_id.setdefault(
                char_id,
                {
                    "char_id": char_id,
                    "name": character.get("name", ""),
                    "appearance": character.get("appearance", ""),
                    "emotion_default": character.get("emotion", ""),
                    "pose_default": character.get("pose", ""),
                },
            )
            panel_char_ids.append(char_id)
        if panel_id is not None:
            character_ids_by_panel[panel_id] = panel_char_ids

    dialogues_by_panel = {}
    for panel in dialogue_data:
        if isinstance(panel, dict) and panel.get("panel_id") is not None:
            dialogues_by_panel[panel["panel_id"]] = panel

    panels = []
    for scene in scene_data:
        if not isinstance(scene, dict):
            continue
        panel_id = scene["panel_id"]
        dialogue_panel = dialogues_by_panel.get(panel_id, {"dialogues": [], "narration": ""})
        panels.append(
            {
                "panel_id": panel_id,
                "theme": scene["theme"],
                "scene_description": scene["scene_description"],
                "location": scene["location"],
                "time": scene["time"],
                "camera_angle": scene["camera_angle"],
                "action": scene["action"],
                "emotion": scene["emotion"],
                "characters": character_ids_by_panel.get(panel_id, []),
                "dialogues": dialogue_panel.get("dialogues", []),
                "narration": dialogue_panel.get("narration", ""),
            }
        )

    final_output = {
        "story_summary": state["prompt"],
        "theme": scene_data[0]["theme"] if scene_data else "",
        "characters": list(characters_by_id.values()),
        "panels": panels,
    }

    is_valid, error = validate_master(final_output)
    if not is_valid:
        raise ValueError(f"Final merged output does not match schema: {error}")

    return {
        **state,
        "final_output": final_output,
        "valid": True,
        "abort": False,
    }
