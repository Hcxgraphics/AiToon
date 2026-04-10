from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from image_gen.core.config import DEFAULT_IMAGE_SIZE, DEFAULT_NEGATIVE_PROMPT, get_output_path


@dataclass(frozen=True)
class DialogueLine:
    text: str
    tone: str = "neutral"
    bubble_type: str = "Speech: oval"
    position_hint: str = "left"
    speaker_id: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "DialogueLine":
        return cls(
            text=str(payload.get("text", "")).strip(),
            tone=str(payload.get("tone", "neutral")).strip(),
            bubble_type=str(payload.get("bubble_type", "Speech: oval")).strip(),
            position_hint=str(payload.get("position_hint", "left")).strip(),
            speaker_id=payload.get("char_id") or payload.get("speaker_id"),
        )


@dataclass(frozen=True)
class SceneTask:
    panel_id: int
    theme: str
    scene_description: str
    location: str
    time_of_day: str
    camera_angle: str
    action: str
    emotion: str
    character_ids: List[str]
    dialogues: List[DialogueLine] = field(default_factory=list)
    importance: str = "normal"
    seed: int = 42
    width: int = DEFAULT_IMAGE_SIZE[0]
    height: int = DEFAULT_IMAGE_SIZE[1]
    style_notes: str = ""
    negative_prompt: str = DEFAULT_NEGATIVE_PROMPT
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def output_path(self) -> Path:
        return get_output_path(self.panel_id)

    @classmethod
    def from_panel(
        cls,
        panel: Dict[str, Any],
        default_theme: Optional[str] = None,
        payload_characters: Optional[Dict[str, Dict[str, Any]]] = None,
        story_summary: str = "",
    ) -> "SceneTask":
        dialogues = [DialogueLine.from_dict(item) for item in panel.get("dialogues", [])]
        return cls(
            panel_id=int(panel["panel_id"]),
            theme=str(panel.get("theme") or default_theme or "Anime").strip(),
            scene_description=str(panel.get("scene_description", "")).strip(),
            location=str(panel.get("location", "unspecified location")).strip(),
            time_of_day=str(panel.get("time", "unspecified time")).strip(),
            camera_angle=str(panel.get("camera_angle", "cinematic panel shot")).strip(),
            action=str(panel.get("action", "story progression moment")).strip(),
            emotion=str(panel.get("emotion", "neutral")).strip(),
            character_ids=[str(char_id) for char_id in panel.get("characters", [])],
            dialogues=dialogues,
            importance=str(panel.get("importance") or panel.get("panel_importance") or "normal").strip(),
            seed=int(panel.get("seed", 42)),
            width=int(panel.get("width", DEFAULT_IMAGE_SIZE[0])),
            height=int(panel.get("height", DEFAULT_IMAGE_SIZE[1])),
            style_notes=str(panel.get("style_notes", "")).strip(),
            negative_prompt=str(panel.get("negative_prompt", DEFAULT_NEGATIVE_PROMPT)).strip(),
            metadata={
                "raw_panel": panel,
                "payload_characters": payload_characters or {},
                "story_summary": story_summary.strip(),
            },
        )


@dataclass(frozen=True)
class CharacterContext:
    char_id: str
    name: str
    appearance: str
    outfit: str
    emotion: str
    pose: str
    anchor_token: str = ""
    identity_prompt: str = ""
    reference_image: Optional[str] = None
    extra_attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PromptPackage:
    positive_prompt: str
    negative_prompt: str
    reference_image: Optional[str]
    prompt_sections: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RoutingDecision:
    primary_model: str
    fallback_models: List[str]
    complexity_score: int
    reasons: List[str]


@dataclass(frozen=True)
class GenerationExecution:
    output_path: str
    model_used: str
    fallback_used: bool
    attempts: int


@dataclass(frozen=True)
class RenderArtifact:
    panel_id: int
    output_path: str
    model_used: str
    prompt: str
    fallback_used: bool
    attempts: int
    success: bool
    error_message: Optional[str] = None
