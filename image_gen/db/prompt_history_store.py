from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from image_gen.db.mongo import get_db

_FALLBACK_PROMPT_HISTORY: Dict[int, Dict[str, Any]] = {}


class PromptHistoryStore:
    """DB-backed prompt history store with version-aware updates per panel."""

    def __init__(self, collection_name: str = "prompt_history"):
        self.collection_name = collection_name

    def save_prompt_history(self, panel_id: int, prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        panel_id = int(panel_id)
        existing = self.fetch_prompt_history(panel_id) or {}
        timestamp = datetime.now(timezone.utc).isoformat()
        final_render_prompt = str(
            prompt_data.get("final_render_prompt")
            or prompt_data.get("optimized_regeneration_prompt")
            or prompt_data.get("original_prompt")
            or existing.get("final_render_prompt", "")
        ).strip()
        original_prompt = str(
            existing.get("original_prompt")
            or prompt_data.get("original_prompt")
            or final_render_prompt
        ).strip()
        prompt_versions = list(existing.get("prompt_versions", []))
        if final_render_prompt and final_render_prompt not in prompt_versions:
            prompt_versions.append(final_render_prompt)

        merged_record = {
            "panel_id": panel_id,
            "original_prompt": original_prompt,
            "final_render_prompt": final_render_prompt,
            "character_anchor_tokens": self._merge_unique_lists(
                existing.get("character_anchor_tokens", []),
                prompt_data.get("character_anchor_tokens", []),
            ),
            "scene_metadata": prompt_data.get("scene_metadata") or existing.get("scene_metadata", {}),
            "generation_timestamp": timestamp,
            "prompt_versions": prompt_versions,
            "last_model_used": prompt_data.get("last_model_used") or existing.get("last_model_used"),
            "latest_regeneration_instruction": prompt_data.get("latest_regeneration_instruction")
            or existing.get("latest_regeneration_instruction"),
        }

        collection = self._get_collection()
        if collection is not None:
            collection.update_one({"panel_id": panel_id}, {"$set": merged_record}, upsert=True)
            return merged_record

        _FALLBACK_PROMPT_HISTORY[panel_id] = deepcopy(merged_record)
        return merged_record

    def fetch_prompt_history(self, panel_id: int) -> Optional[Dict[str, Any]]:
        collection = self._get_collection()
        if collection is not None:
            record = collection.find_one({"panel_id": int(panel_id)}, {"_id": 0})
            if record:
                return record
        fallback = _FALLBACK_PROMPT_HISTORY.get(int(panel_id))
        return deepcopy(fallback) if fallback else None

    def _get_collection(self):
        database = get_db()
        if database is None:
            return None
        return database[self.collection_name]

    @staticmethod
    def _merge_unique_lists(*lists: Any) -> list[str]:
        merged: list[str] = []
        for values in lists:
            for value in values or []:
                item = str(value).strip()
                if item and item not in merged:
                    merged.append(item)
        return merged
