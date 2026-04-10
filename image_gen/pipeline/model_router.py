from __future__ import annotations

from typing import List

from image_gen.core.config import get_default_model, get_model_fallbacks
from image_gen.core.contracts import RoutingDecision, SceneTask


class SceneModelRouter:
    """Rule-based router for choosing the best model for each scene."""

    def route(self, scene: SceneTask) -> RoutingDecision:
        complexity_score = self._score_complexity(scene)
        if self._is_high_priority_final(scene, complexity_score):
            primary = "sdxl"
        elif len(scene.character_ids) >= 2 or complexity_score >= 5:
            primary = "lightning"
        elif complexity_score <= 1:
            primary = "flux"
        else:
            primary = get_default_model()

        return RoutingDecision(
            primary_model=primary,
            fallback_models=list(get_model_fallbacks(primary)),
            complexity_score=complexity_score,
            reasons=self._build_reasons(scene, complexity_score),
        )

    @staticmethod
    def _score_complexity(scene: SceneTask) -> int:
        score = 0
        score += min(len(scene.character_ids), 3)
        score += min(len(scene.dialogues), 2)
        cinematic_terms = (
            f"{scene.scene_description} {scene.action} {scene.camera_angle} {scene.emotion}".lower()
        )
        if any(term in cinematic_terms for term in ("battle", "crowd", "ruins", "magic", "storm", "explosion")):
            score += 2
        if any(term in cinematic_terms for term in ("close-up", "extreme", "dramatic", "wide", "cinematic")):
            score += 1
        if str(scene.importance).lower() in {"high", "hero", "key", "climax", "critical"}:
            score += 2
        return score

    @staticmethod
    def _is_high_priority_final(scene: SceneTask, complexity_score: int) -> bool:
        return str(scene.importance).lower() in {"high", "hero", "key", "climax", "critical"} or complexity_score >= 7

    @staticmethod
    def _build_reasons(scene: SceneTask, complexity_score: int) -> List[str]:
        return [
            f"complexity_score={complexity_score}",
            f"characters={len(scene.character_ids)}",
            f"dialogues={len(scene.dialogues)}",
            f"importance={scene.importance}",
            f"camera_angle={scene.camera_angle}",
        ]
