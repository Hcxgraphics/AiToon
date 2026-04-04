from prompt_toolkit import prompt

from config.db import get_db
from services.character_service import CharacterService

PERSISTENT_FIELDS = { #These define character identity.
    "name",
    "gender",
    "face_shape",
    "hair_style",
    "hair_color",
    "body_type",
    "default_clothing"
}

DYNAMIC_FIELDS = { #These must come from prompt / scene / story
    "emotion",
    "pose",
    "action",
    "clothing_override",
    "art_style"
}

service = CharacterService(get_db())

def split_character_fields(character):
    persistent = {}
    dynamic = {}

    for key, value in character.items():
        if key in PERSISTENT_FIELDS:
            persistent[key] = value
        elif key in DYNAMIC_FIELDS:
            dynamic[key] = value

    return persistent, dynamic


def character_resolver_node(state):
    character_data = state["character_data"]
    resolved_character_data = []

    for panel in character_data:
        if not isinstance(panel, dict):
            resolved_character_data.append(panel)
            continue

        characters = panel.get("characters")
        if not isinstance(characters, list):
            resolved_character_data.append(panel)
            continue

        resolved_panel_characters = []
        for char in characters:
            persistent, dynamic = split_character_fields(char)
            matched = service.resolve_character(state.get("user_id", "test_user"), persistent)

            resolved_character = {
                **matched,
                **dynamic
            }
            if "id" not in resolved_character and char.get("char_id"):
                resolved_character["id"] = str(char["char_id"])
            if "char_id" not in resolved_character and char.get("char_id"):
                resolved_character["char_id"] = str(char["char_id"])

            resolved_panel_characters.append(resolved_character)

        resolved_character_data.append({
            **panel,
            "characters": resolved_panel_characters,
        })

    state["character_data"] = resolved_character_data
    return state
