from __future__ import annotations

from image_gen.core.config import has_pixazo_api_key
from image_gen.pipeline.batch_renderer import BatchRenderer
from image_gen.pipeline.task_splitter import SceneTaskSplitter

SAMPLE_ORCHESTRATOR_PAYLOAD = {
    "final_output": {
        "theme": "Anime",
        "characters": [
            {
                "char_id": "c1",
                "name": "Luna",
                "appearance": "young lunar mage with silver hair and glowing blue eyes",
                "emotion_default": "Determined",
                "pose_default": "Standing",
            },
            {
                "char_id": "c2",
                "name": "Kai",
                "appearance": "charismatic treasure hunter with tousled dark hair and sharp amber eyes",
                "emotion_default": "Focused",
                "pose_default": "Standing",
            },
        ],
        "panels": [
            {
                "panel_id": 1,
                "scene_description": "Luna discovers a prophecy on a moonlit stone tablet above ancient ruins.",
                "location": "cliff overlooking ancient ruins",
                "time": "Night",
                "camera_angle": "wide shot capturing the moon and ruins",
                "action": "Luna studies the glowing inscription while wind moves her cloak.",
                "emotion": "Determined",
                "characters": ["c1"],
            },
            {
                "panel_id": 2,
                "scene_description": "Kai unfolds an old map in a dim tavern lit by lantern glow.",
                "location": "tavern",
                "time": "Evening",
                "camera_angle": "close-up on Kai's face and the map",
                "action": "Kai plots the route to the moonstone.",
                "emotion": "Excited",
                "characters": ["c2"],
            },
        ],
    }
}


if __name__ == "__main__":
    tasks = SceneTaskSplitter().split(SAMPLE_ORCHESTRATOR_PAYLOAD)
    print(f"Prepared {len(tasks)} scene tasks")

    if not has_pixazo_api_key():
        print("Skipping remote render smoke test because no Pixazo API key is configured.")
    else:
        results = BatchRenderer().render_payload(SAMPLE_ORCHESTRATOR_PAYLOAD)
        for result in results:
            print(result)
