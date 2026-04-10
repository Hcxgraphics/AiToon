from __future__ import annotations

from typing import Iterable, List

from image_gen.core.contracts import CharacterContext, PromptPackage, SceneTask
from image_gen.core.logger import get_logger
from image_gen.prompt_engine.theme_mapper import get_theme_style, normalize_theme

logger = get_logger(__name__)


class ScenePromptBuilder:
    """Creates deterministic, consistency-first prompts for panel generation."""

    def build(self, scene: SceneTask, characters: Iterable[CharacterContext]) -> PromptPackage:
        character_list = list(characters)
        normalized_theme = normalize_theme(scene.theme)
        scene_description = self._compose_scene_description(scene)
        character_blocks = self._build_character_blocks(character_list)
        ordered_parts = [
            *character_blocks,
            scene_description,
            scene.camera_angle,
            "cinematic comic panel",
            get_theme_style(normalized_theme),
            "dramatic lighting",
        ]
        if scene.style_notes:
            ordered_parts.append(scene.style_notes)
        positive_prompt = ", ".join(part for part in ordered_parts if part)
        sections = {
            "characters": " | ".join(character_blocks),
            "scene": scene_description,
            "camera_angle": scene.camera_angle,
            "theme": get_theme_style(normalized_theme),
        }
        logger.info("Built prompt for panel=%s", scene.panel_id)
        return PromptPackage(
            positive_prompt=positive_prompt,
            negative_prompt=scene.negative_prompt,
            reference_image=next((item.reference_image for item in character_list if item.reference_image), None),
            prompt_sections=sections,
        )

    def _build_character_blocks(self, characters: List[CharacterContext]) -> List[str]:
        if not characters:
            return ["[SCENE_SIG_V1], environment-focused comic scene, same face, same hairstyle, same costume"]
        return [
            ", ".join(
                [
                    character.anchor_token,
                    character.identity_prompt,
                    "same face",
                    "same hairstyle",
                    "same costume",
                ]
            )
            for character in characters
        ]

    @staticmethod
    def _compose_scene_description(scene: SceneTask) -> str:
        parts = [
            scene.scene_description,
            f"location: {scene.location}",
            f"time: {scene.time_of_day}",
            f"action: {scene.action}",
            f"emotion: {scene.emotion}",
        ]
        if scene.dialogues:
            dialogue_cues = "; ".join(line.text for line in scene.dialogues if line.text)
            if dialogue_cues:
                parts.append(f"dialogue cues: {dialogue_cues}")
        return ", ".join(part for part in parts if part)
