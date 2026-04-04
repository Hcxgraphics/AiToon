from orchestrator.validators.utils import fail_validation, pass_validation


def character_validator(state):
    character_data = state.get("character_data")
    scene_data = state.get("scene_data", [])
    scene_panel_ids = {panel.get("panel_id") for panel in scene_data if isinstance(panel, dict)}

    if not isinstance(character_data, list) or not character_data:
        return fail_validation(state, "character_retries", "character_error", "Character agent returned no data")

    registry = {}
    seen_panel_ids = set()

    for panel in character_data:
        if not isinstance(panel, dict):
            return fail_validation(state, "character_retries", "character_error", "Each character panel must be an object")

        panel_id = panel.get("panel_id")
        if panel_id not in scene_panel_ids:
            return fail_validation(state, "character_retries", "character_error", "Character panel_id does not match scene panel_id")
        if panel_id in seen_panel_ids:
            return fail_validation(state, "character_retries", "character_error", "Character panel_id values must be unique")
        seen_panel_ids.add(panel_id)

        characters = panel.get("characters")
        if not isinstance(characters, list) or not characters:
            return fail_validation(state, "character_retries", "character_error", "Each panel must contain at least one character")

        for character in characters:
            if not isinstance(character, dict):
                return fail_validation(state, "character_retries", "character_error", "Character entries must be objects")

            for key in ("char_id", "name", "appearance", "emotion", "pose"):
                value = character.get(key)
                if not isinstance(value, str) or not value.strip():
                    return fail_validation(
                        state,
                        "character_retries",
                        "character_error",
                        f"Character field '{key}' must be a non-empty string",
                    )

            char_id = character["char_id"]
            fingerprint = (
                character["name"].strip(),
                character["appearance"].strip(),
            )
            if char_id in registry and registry[char_id] != fingerprint:
                return fail_validation(
                    state,
                    "character_retries",
                    "character_error",
                    f"Character '{char_id}' has inconsistent identity fields across panels",
                )
            registry[char_id] = fingerprint

    if seen_panel_ids != scene_panel_ids:
        return fail_validation(
            state,
            "character_retries",
            "character_error",
            "Character output must cover every scene panel_id exactly once",
        )

    return pass_validation(state, "character_error")
