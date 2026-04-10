from __future__ import annotations

import re
from typing import Iterable, List, Optional

from image_gen.core.contracts import CharacterContext, SceneTask
from image_gen.db.character_memory_store import CharacterMemoryStore
from image_gen.db.character_repository import CharacterRepository


class CharacterMemoryService:
    """Builds render-ready character context from AiToon DB and payload metadata."""

    def __init__(
        self,
        repository: Optional[CharacterRepository] = None,
        memory_store: Optional[CharacterMemoryStore] = None,
    ):
        self.repository = repository or CharacterRepository()
        self.memory_store = memory_store or CharacterMemoryStore()

    def get_character_contexts(self, char_ids: Iterable[str], scene: Optional[SceneTask] = None) -> List[CharacterContext]:
        payload_characters = (scene.metadata.get("payload_characters") if scene else {}) or {}
        contexts: List[CharacterContext] = []
        for char_id in char_ids:
            payload_character = payload_characters.get(char_id, {})
            repository_character = self.repository.get_character(char_id) or {}
            memory = self.memory_store.get_character_memory(char_id) or {}
            merged = {**memory, **repository_character, **payload_character}
            contexts.append(self._build_context(char_id=char_id, character=merged, scene=scene))
        return contexts

    def _build_context(self, char_id: str, character: dict, scene: Optional[SceneTask]) -> CharacterContext:
        name = str(character.get("name") or f"Character {char_id}").strip()
        appearance = str(character.get("appearance") or "distinctive comic character appearance").strip()
        outfit = str(
            character.get("outfit")
            or character.get("default_clothing")
            or character.get("clothing")
            or "signature costume"
        ).strip()
        emotion = str(
            scene.emotion if scene and scene.emotion else character.get("emotion_default") or "neutral"
        ).strip()
        pose = str(
            character.get("pose")
            or character.get("pose_default")
            or character.get("default_pose")
            or self._infer_pose(scene)
        ).strip()
        anchor_token = str(character.get("anchor_token") or self._build_anchor_token(name, char_id)).strip()
        identity_prompt = str(character.get("identity_prompt") or appearance).strip()
        return CharacterContext(
            char_id=char_id,
            name=name,
            appearance=appearance,
            outfit=outfit,
            emotion=emotion,
            pose=pose,
            anchor_token=anchor_token,
            identity_prompt=identity_prompt,
            reference_image=character.get("reference_image"),
            extra_attributes={
                "role": character.get("role"),
                "style_tags": character.get("style_tags", []),
            },
        )

    @staticmethod
    def _build_anchor_token(name: str, char_id: str) -> str:
        slug = re.sub(r"[^A-Z0-9]+", "_", name.upper()).strip("_") or char_id.upper()
        return f"[{slug}_SIG_V1]"

    @staticmethod
    def _infer_pose(scene: Optional[SceneTask]) -> str:
        if not scene or not scene.action:
            return "story-driven pose"
        lowered = scene.action.lower()
        if any(token in lowered for token in ("run", "sprint", "chase")):
            return "dynamic running pose"
        if any(token in lowered for token in ("fight", "attack", "strike", "battle")):
            return "combat-ready pose"
        if any(token in lowered for token in ("look", "watch", "gaze", "discover")):
            return "focused observational pose"
        return "story-driven pose"
