from __future__ import annotations

from pathlib import Path

from image_gen.core.config import has_pixazo_api_key
from image_gen.pipeline.batch_renderer import BatchRenderer

BIG_PROMPT_PAYLOAD = {
    "final_output": {
        "theme": "Fantasy",
        "characters": [
            {
                "char_id": "c1",
                "name": "Luna",
                "appearance": "young female mage with silver hair and glowing blue eyes",
                "emotion_default": "Determined",
                "pose_default": "Standing heroically with an arcane staff",
            }
        ],
        "panels": [
            {
                "panel_id": 101,
                "theme": "Fantasy",
                "scene_description": (
                    "An epic moonlit cliffside citadel rises above a storm-torn sea while ancient floating runes, "
                    "shattered pillars, drifting fog, and glowing lanterns frame Luna at the center."
                ),
                "location": "moonlit cliffside citadel above a stormy ocean",
                "time": "Midnight",
                "camera_angle": "wide cinematic hero shot with dramatic perspective",
                "action": "Luna raises an ancient crystal staff as a protective arcane barrier forms overhead.",
                "emotion": "Determined",
                "characters": ["c1"],
                "importance": "climax",
                "style_notes": "premium key art quality, luminous magic effects, strong rim lighting",
                "seed": 77,
            }
        ],
    }
}


if __name__ == "__main__":
    if not has_pixazo_api_key():
        print("Set AITOON_PIXAZO_API_KEY in image_gen/.env.image_gen before running this script.")
    else:
        results = BatchRenderer().render_payload(BIG_PROMPT_PAYLOAD)
        for result in results:
            output = Path(result.output_path)
            print(result)
            if not result.success:
                raise RuntimeError(f"Big prompt render failed: {result.error_message}")
            if not output.exists():
                raise FileNotFoundError(f"Expected output missing: {output}")
        print("Big prompt pipeline test completed successfully.")
