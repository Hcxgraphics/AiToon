from orchestrator.validators.utils import fail_validation, pass_validation


def scene_validator(state):
    scenes = state.get("scene_data")
    constraints = state.get("constraints", {})
    allowed_themes = set(constraints.get("themes", []))

    if not isinstance(scenes, list) or not scenes:
        return fail_validation(state, "scene_retries", "scene_error", "Scene agent returned no panels")

    required_keys = {
        "panel_id",
        "theme",
        "scene_description",
        "location",
        "time",
        "camera_angle",
        "action",
        "emotion",
    }
    seen_panel_ids = set()

    for panel in scenes:
        if not isinstance(panel, dict):
            return fail_validation(state, "scene_retries", "scene_error", "Each scene panel must be an object")

        missing = sorted(required_keys - panel.keys())
        if missing:
            return fail_validation(
                state,
                "scene_retries",
                "scene_error",
                f"Scene panel is missing fields: {', '.join(missing)}",
            )

        panel_id = panel.get("panel_id")
        if not isinstance(panel_id, int) or panel_id < 1:
            return fail_validation(state, "scene_retries", "scene_error", "panel_id must be a positive integer")
        if panel_id in seen_panel_ids:
            return fail_validation(state, "scene_retries", "scene_error", "panel_id values must be unique")
        seen_panel_ids.add(panel_id)

        theme = panel.get("theme")
        if theme not in allowed_themes:
            return fail_validation(
                state,
                "scene_retries",
                "scene_error",
                f"theme '{theme}' is not allowed by MongoDB constraints",
            )

        for key in required_keys - {"panel_id"}:
            if not isinstance(panel.get(key), str) or not panel[key].strip():
                return fail_validation(
                    state,
                    "scene_retries",
                    "scene_error",
                    f"Scene field '{key}' must be a non-empty string",
                )

    return pass_validation(state, "scene_error")
