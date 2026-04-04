from typing import Dict, Any, Optional, Tuple
from copy import deepcopy
from config.db import get_db
from bson import ObjectId


class CharacterService:
    """
    Handles character lookup, matching, merging,
    and safe creation in user library.
    """

    PERSISTENT_FIELDS = {
        "name",
        "gender",
        "age_group",
        "face_shape",
        "hair_style",
        "hair_color",
        "body_type",
        "skin_tone",
        "default_clothing",
        "art_style"
    }

    DYNAMIC_FIELDS = {
        "emotion",
        "pose",
        "action",
        "expression",
        "clothing_override",
        "camera_angle",
        "panel_position"
    }

    MATCH_FIELDS = {
        "face_shape",
        "hair_style",
        "hair_color",
        "body_type",
        "art_style"
    }

    EXACT_MATCH_THRESHOLD = 0.90
    PARTIAL_MATCH_THRESHOLD = 0.70

    def __init__(self, db):
        self.db = db
        self.primary_collection = db.primary_characters
        self.user_collection = db.user_characters

    # =========================================================
    # PUBLIC MAIN METHOD
    # =========================================================
    def resolve_character(
        self,
        user_id: str,
        incoming_character: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Main resolver method.

        Flow:
        1. Split persistent/dynamic fields
        2. Search primary library
        3. Search user library
        4. Merge missing fields if needed
        5. Create new character if partial mismatch
        """

        persistent, dynamic = self.split_character_fields(
            incoming_character
        )

        # 1. Check primary library
        primary_match, primary_score = self.find_best_match(
            self.primary_collection,
            persistent,
            extra_filter={}
        )

        if primary_match and primary_score >= self.EXACT_MATCH_THRESHOLD:
            return self.build_runtime_character(
                primary_match,
                dynamic
            )

        # 2. Check user library
        user_match, user_score = self.find_best_match(
            self.user_collection,
            persistent,
            extra_filter={"user_id": user_id}
        )

        if user_match:
            # exact match
            if user_score >= self.EXACT_MATCH_THRESHOLD:
                merged = self.merge_missing_attributes(
                    user_match,
                    persistent
                )
                return self.build_runtime_character(
                    merged,
                    dynamic
                )

            # enough similarity + missing fields
            if (
                user_score >= self.PARTIAL_MATCH_THRESHOLD
                and self.has_missing_fields(persistent)
            ):
                merged = self.merge_missing_attributes(
                    user_match,
                    persistent
                )
                saved = self.create_user_character(
                    user_id,
                    merged,
                    base_character_id=user_match.get("_id")
                )
                return self.build_runtime_character(
                    saved,
                    dynamic
                )

        # 3. Partial similarity should create new character
        new_character = self.create_user_character(
            user_id,
            persistent
        )

        return self.build_runtime_character(
            new_character,
            dynamic
        )

    # =========================================================
    # FIELD SPLITTING
    # =========================================================
    def split_character_fields(
        self,
        character: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        persistent = {}
        dynamic = {}

        for key, value in character.items():
            if key in self.PERSISTENT_FIELDS:
                persistent[key] = value
            elif key in self.DYNAMIC_FIELDS:
                dynamic[key] = value

        return persistent, dynamic

    # =========================================================
    # MATCHING
    # =========================================================
    def find_best_match(
        self,
        collection,
        incoming: Dict[str, Any],
        extra_filter: Dict[str, Any]
    ) -> Tuple[Optional[Dict[str, Any]], float]:

        candidates = list(collection.find(extra_filter))

        best_match = None
        best_score = 0.0

        for candidate in candidates:
            score = self.compute_similarity_score(
                incoming,
                candidate
            )

            if score > best_score:
                best_score = score
                best_match = candidate

        return best_match, best_score

    def compute_similarity_score(
        self,
        incoming: Dict[str, Any],
        saved: Dict[str, Any]
    ) -> float:
        total_fields = len(self.MATCH_FIELDS)
        matched = 0

        for field in self.MATCH_FIELDS:
            incoming_value = incoming.get(field)
            saved_value = saved.get(field)

            if (
                incoming_value is not None
                and saved_value is not None
                and incoming_value == saved_value
            ):
                matched += 1

        return matched / total_fields if total_fields > 0 else 0.0

    # =========================================================
    # MERGING
    # =========================================================
    def merge_missing_attributes(
        self,
        saved: Dict[str, Any],
        incoming: Dict[str, Any]
    ) -> Dict[str, Any]:
        merged = deepcopy(saved)

        for key, value in incoming.items():
            if value not in [None, "", "unknown"]:
                merged[key] = value

        return merged

    def has_missing_fields(
        self,
        character: Dict[str, Any]
    ) -> bool:
        for field in self.MATCH_FIELDS:
            if character.get(field) in [None, "", "unknown"]:
                return True
        return False

    # =========================================================
    # CREATION
    # =========================================================
    def create_user_character(
        self,
        user_id: str,
        character_data: Dict[str, Any],
        base_character_id: Optional[Any] = None
    ) -> Dict[str, Any]:
        document = {
            "user_id": user_id,
            "base_character_id": str(base_character_id)
            if base_character_id else None,
            **character_data
        }

        result = self.user_collection.insert_one(document)

        return self.user_collection.find_one(
            {"_id": result.inserted_id}
        )

    # =========================================================
    # RUNTIME OUTPUT
    # =========================================================
    def build_runtime_character(
        self,
        saved_character: Dict[str, Any],
        dynamic: Dict[str, Any]
    ) -> Dict[str, Any]:
        runtime_character = deepcopy(saved_character)

        # clothing override only for runtime
        runtime_character["clothing"] = (
            dynamic.get("clothing_override")
            or saved_character.get("default_clothing")
        )

        # add dynamic fields only in runtime
        runtime_character.update(dynamic)

        return runtime_character