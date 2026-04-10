from __future__ import annotations

from typing import Dict, List, Optional

from image_gen.db.mongo import get_db

FALLBACK_CHARACTERS: Dict[str, Dict[str, str]] = {
    "c1": {
        "char_id": "c1",
        "name": "Luna",
        "appearance": "young lunar mage with silver hair and glowing blue eyes",
        "outfit": "layered moonlit mage robes with an ornate artifact belt",
        "emotion_default": "determined",
        "pose_default": "standing with a glowing artifact",
        "identity_prompt": "young female mage with silver hair and glowing blue eyes",
        "anchor_token": "[LUNA_SIG_V1]",
    },
    "c2": {
        "char_id": "c2",
        "name": "Kai",
        "appearance": "charismatic treasure hunter with tousled dark hair and sharp amber eyes",
        "outfit": "adventurer coat with belts, satchel, and relic-hunting gear",
        "emotion_default": "focused",
        "pose_default": "confident explorer stance",
        "identity_prompt": "young male treasure hunter with tousled dark hair and sharp amber eyes",
        "anchor_token": "[KAI_SIG_V1]",
    },
    "c3": {
        "char_id": "c3",
        "name": "Rex",
        "appearance": "rugged beastmaster with broad shoulders, wild hair, and a weathered expression",
        "outfit": "fur-lined wilderness gear with creature-handler accessories",
        "emotion_default": "confident",
        "pose_default": "steady command pose beside mythical beasts",
        "identity_prompt": "rugged male beastmaster with wild hair and a weathered expression",
        "anchor_token": "[REX_SIG_V1]",
    },
}


class CharacterRepository:
    """Read-only character access via the AiToon DB."""

    def __init__(self, collection_name: str = "characters"):
        self.collection_name = collection_name

    def get_character(self, char_id: str) -> Optional[Dict]:
        collection = self._get_collection()
        if collection is not None:
            document = collection.find_one({"char_id": char_id}, {"_id": 0})
            if document:
                return document
        return FALLBACK_CHARACTERS.get(char_id)

    def get_multiple(self, char_ids: List[str]) -> List[Dict]:
        collection = self._get_collection()
        if collection is not None:
            records = list(collection.find({"char_id": {"$in": char_ids}}, {"_id": 0}))
            if records:
                by_id = {record["char_id"]: record for record in records if "char_id" in record}
                return [by_id[char_id] for char_id in char_ids if char_id in by_id]
        return [FALLBACK_CHARACTERS[char_id] for char_id in char_ids if char_id in FALLBACK_CHARACTERS]

    def _get_collection(self):
        database = get_db()
        if database is None:
            return None
        return database[self.collection_name]
