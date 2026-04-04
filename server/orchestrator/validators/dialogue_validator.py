from orchestrator.logger import get_logger
from orchestrator.validators.utils import fail_validation, pass_validation


logger = get_logger("orchestrator.validators.dialogue_validator")


def dialogue_validator(state):
    dialogue_data = state.get("dialogue_data")
    scene_data = state.get("scene_data", [])
    character_data = state.get("character_data", [])
    allowed_bubbles = set(state.get("constraints", {}).get("bubble_types", []))

    if not isinstance(dialogue_data, list) or not dialogue_data:
        return fail_validation(state, "dialogue_retries", "dialogue_error", "Dialogue agent returned no data")

    expected_panel_ids = {panel.get("panel_id") for panel in scene_data if isinstance(panel, dict)}
    seen_panel_ids = set()

    valid_ids = set()
    name_to_id = {}
    for character in character_data:
        if not isinstance(character, dict):
            continue

        if isinstance(character.get("characters"), list):
            for nested_character in character.get("characters", []):
                if not isinstance(nested_character, dict):
                    continue
                nested_id = nested_character.get("char_id", nested_character.get("id", nested_character.get("_id")))
                if nested_id is not None:
                    normalized_nested_id = str(nested_id)
                    valid_ids.add(normalized_nested_id)
                    if isinstance(nested_character.get("name"), str) and nested_character["name"].strip():
                        name_to_id[nested_character["name"]] = normalized_nested_id
            continue

        character_id = character.get("id", character.get("_id", character.get("char_id")))
        if character_id is not None:
            normalized_id = str(character_id)
            valid_ids.add(normalized_id)
            if isinstance(character.get("name"), str) and character["name"].strip():
                name_to_id[character["name"]] = normalized_id

    for panel in dialogue_data:
        if not isinstance(panel, dict):
            return fail_validation(state, "dialogue_retries", "dialogue_error", "Each dialogue panel must be an object")

        panel_id = panel.get("panel_id")
        if panel_id not in expected_panel_ids:
            return fail_validation(state, "dialogue_retries", "dialogue_error", "Dialogue panel_id does not match scene panel_id")
        if panel_id in seen_panel_ids:
            return fail_validation(state, "dialogue_retries", "dialogue_error", "Dialogue panel_id values must be unique")
        seen_panel_ids.add(panel_id)

        dialogues = panel.get("dialogues")
        if not isinstance(dialogues, list):
            return fail_validation(state, "dialogue_retries", "dialogue_error", "Dialogue panel must contain a dialogues list")

        narration = panel.get("narration")
        if not isinstance(narration, str):
            return fail_validation(state, "dialogue_retries", "dialogue_error", "Dialogue panel narration must be a string")

        logger.debug("Characters: %s", character_data)
        logger.debug("Dialogues: %s", dialogues)

        for dialogue in dialogues:
            if not isinstance(dialogue, dict):
                return fail_validation(state, "dialogue_retries", "dialogue_error", "Dialogue entries must be objects")

            for key in ("char_id", "text", "tone", "bubble_type", "position_hint"):
                value = dialogue.get(key)
                if not isinstance(value, str) or not value.strip():
                    return fail_validation(
                        state,
                        "dialogue_retries",
                        "dialogue_error",
                        f"Dialogue field '{key}' must be a non-empty string",
                    )

            dialogue["char_id"] = str(dialogue["char_id"])
            if dialogue["char_id"] not in valid_ids:
                match = name_to_id.get(dialogue.get("speaker"))
                if match:
                    dialogue["char_id"] = match
                else:
                    return fail_validation(
                        state,
                        "dialogue_retries",
                        "dialogue_error",
                        f"Dialogue references unknown char_id '{dialogue['char_id']}'",
                    )

            if dialogue["bubble_type"] not in allowed_bubbles:
                return fail_validation(
                    state,
                    "dialogue_retries",
                    "dialogue_error",
                    f"bubble_type '{dialogue['bubble_type']}' is not allowed by MongoDB constraints",
                )

    if seen_panel_ids != expected_panel_ids:
        return fail_validation(state, "dialogue_retries", "dialogue_error", "Dialogue output must cover every scene panel_id exactly once")

    return pass_validation(state, "dialogue_error")
