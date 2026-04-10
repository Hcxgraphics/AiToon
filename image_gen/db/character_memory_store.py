from __future__ import annotations

from typing import Dict, List, Optional

from image_gen.db.mongo import get_db

FALLBACK_CHARACTER_MEMORY: Dict[str, Dict[str, str]] = {
    "c1": {
        "char_id": "c1",
        "anchor_token": "[LUNA_SIG_V1]",
        "identity_prompt": "young female mage with silver hair and glowing blue eyes",
        "emotion_default": "Determined",
        "pose_default": "Standing",
    },
    "c2": {
        "char_id": "c2",
        "anchor_token": "[KAI_SIG_V1]",
        "identity_prompt": "young male treasure hunter with tousled dark hair and sharp amber eyes",
        "emotion_default": "Focused",
        "pose_default": "Standing",
    },
    "c3": {
        "char_id": "c3",
        "anchor_token": "[REX_SIG_V1]",
        "identity_prompt": "rugged male beastmaster with wild hair and a weathered expression",
        "emotion_default": "Confident",
        "pose_default": "Standing",
    },
}


class CharacterMemoryStore:
    """Persistent anchor-token store backed by the AiToon DB."""

    def __init__(self, collection_name: str = "character_memory"):
        self.collection_name = collection_name

    def get_character_memory(self, char_id: str) -> Optional[Dict[str, str]]:
        collection = self._get_collection()
        if collection is not None:
            record = collection.find_one({"char_id": char_id}, {"_id": 0})
            if record:
                return record
        return FALLBACK_CHARACTER_MEMORY.get(char_id)

    def get_multiple(self, char_ids: List[str]) -> List[Dict[str, str]]:
        collection = self._get_collection()
        if collection is not None:
            records = list(collection.find({"char_id": {"$in": char_ids}}, {"_id": 0}))
            if records:
                by_id = {record["char_id"]: record for record in records if "char_id" in record}
                return [by_id[char_id] for char_id in char_ids if char_id in by_id]
        return [FALLBACK_CHARACTER_MEMORY[char_id] for char_id in char_ids if char_id in FALLBACK_CHARACTER_MEMORY]

    def upsert_character_memory(self, record: Dict[str, str]) -> None:
        collection = self._get_collection()
        if collection is None:
            char_id = record.get("char_id")
            if char_id:
                FALLBACK_CHARACTER_MEMORY[char_id] = record
            return
        collection.update_one({"char_id": record["char_id"]}, {"$set": record}, upsert=True)

    def _get_collection(self):
        database = get_db()
        if database is None:
            return None
        return database[self.collection_name]
