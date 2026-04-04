from orchestrator.core.graph import run_pipeline
from orchestrator.logger import get_logger


DEFAULT_BUBBLE_TYPES = ["Speech: oval", "Speech: rectangle", "Thought (Cloud like)" , "Whisper (Dashed or faint outline)", "Shout(Jagged / spiky)", "Robot Electronic (Zigzag or geometric)"]

logger = get_logger("services.ai_service")


def run_orchestrator(prompt, theme, user_id="test_user"):
    selected_theme = theme or "Anime"
    logger.info("Running orchestrator for theme=%s", selected_theme)

    def constraints_provider():
        return {
            "themes": [selected_theme],
            "bubble_types": DEFAULT_BUBBLE_TYPES,
        }

    return run_pipeline(
        user_input=prompt,
        constraints_provider=constraints_provider,
        user_id=user_id,
    )
