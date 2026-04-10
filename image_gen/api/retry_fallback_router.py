from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from image_gen.api.pixazo_client import PixazoClient
from image_gen.core.config import BATCH_CONFIG, get_default_model, get_model_fallbacks, normalize_model_name
from image_gen.core.contracts import GenerationExecution, PromptPackage, SceneTask
from image_gen.core.logger import get_logger
from image_gen.pipeline.model_router import SceneModelRouter
from image_gen.prompt_engine.character_memory import CharacterMemoryService
from image_gen.prompt_engine.prompt_builder import ScenePromptBuilder

logger = get_logger(__name__)


class RetryFallbackRouter:
    """Retries panel generation and walks configured model fallbacks."""

    def __init__(
        self,
        client: Optional[PixazoClient] = None,
        router: Optional[SceneModelRouter] = None,
        prompt_builder: Optional[ScenePromptBuilder] = None,
        character_memory: Optional[CharacterMemoryService] = None,
    ):
        self.client = client or PixazoClient()
        self.router = router or SceneModelRouter()
        self.prompt_builder = prompt_builder or ScenePromptBuilder()
        self.character_memory = character_memory or CharacterMemoryService()

    def build_prompt_package(self, scene_task: SceneTask) -> PromptPackage:
        character_contexts = self.character_memory.get_character_contexts(scene_task.character_ids, scene=scene_task)
        return self.prompt_builder.build(scene_task, character_contexts)

    def render_with_retry(
        self,
        scene_task: SceneTask,
        retries: Optional[int] = None,
        prompt_package: Optional[PromptPackage] = None,
    ) -> GenerationExecution:
        max_retries = retries or BATCH_CONFIG.max_retries
        package = prompt_package or self.build_prompt_package(scene_task)
        decision = self.router.route(scene_task)
        candidate_models = [decision.primary_model, *decision.fallback_models]
        last_error: Optional[Exception] = None

        for model_index, model_name in enumerate(candidate_models):
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(
                        "Rendering panel=%s with model=%s attempt=%s/%s",
                        scene_task.panel_id,
                        model_name,
                        attempt,
                        max_retries,
                    )
                    image = self.client.generate(
                        model_name=model_name,
                        prompt=package.positive_prompt,
                        negative_prompt=package.negative_prompt,
                        width=scene_task.width,
                        height=scene_task.height,
                        seed=scene_task.seed,
                    )
                    scene_task.output_path.parent.mkdir(parents=True, exist_ok=True)
                    image.save(scene_task.output_path)
                    return GenerationExecution(
                        output_path=str(scene_task.output_path),
                        model_used=model_name,
                        fallback_used=model_index > 0,
                        attempts=attempt,
                    )
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    logger.warning(
                        "Generation failed for panel=%s model=%s attempt=%s/%s: %s",
                        scene_task.panel_id,
                        model_name,
                        attempt,
                        max_retries,
                        exc,
                    )
                    if attempt < max_retries:
                        time.sleep(BATCH_CONFIG.retry_backoff_seconds * (2 ** (attempt - 1)))
            logger.info("Falling back from model=%s for panel=%s", model_name, scene_task.panel_id)

        raise RuntimeError(
            f"Unable to render panel {scene_task.panel_id} after retries and fallbacks: {last_error}"
        )

    def regenerate_with_retry(
        self,
        *,
        panel_id: int,
        prompt: str,
        output_path: str,
        preferred_model: str | None = None,
        retries: Optional[int] = None,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: int = 42,
    ) -> GenerationExecution:
        max_retries = retries or BATCH_CONFIG.max_retries
        candidate_models = self._build_regeneration_chain(preferred_model)
        last_error: Optional[Exception] = None
        output = Path(output_path)

        for model_index, model_name in enumerate(candidate_models):
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(
                        "Regenerating panel=%s with model=%s attempt=%s/%s",
                        panel_id,
                        model_name,
                        attempt,
                        max_retries,
                    )
                    image = self.client.generate(
                        model_name=model_name,
                        prompt=prompt,
                        negative_prompt=negative_prompt,
                        width=width,
                        height=height,
                        seed=seed,
                    )
                    output.parent.mkdir(parents=True, exist_ok=True)
                    image.save(output)
                    return GenerationExecution(
                        output_path=str(output),
                        model_used=model_name,
                        fallback_used=model_index > 0,
                        attempts=attempt,
                    )
                except Exception as exc:  # noqa: BLE001
                    last_error = exc
                    logger.warning(
                        "Regeneration failed for panel=%s model=%s attempt=%s/%s: %s",
                        panel_id,
                        model_name,
                        attempt,
                        max_retries,
                        exc,
                    )
                    if attempt < max_retries:
                        time.sleep(BATCH_CONFIG.retry_backoff_seconds * (2 ** (attempt - 1)))
            logger.info("Falling back from regeneration model=%s for panel=%s", model_name, panel_id)

        raise RuntimeError(
            f"Unable to regenerate panel {panel_id} after retries and fallbacks: {last_error}"
        )

    @staticmethod
    def _build_regeneration_chain(preferred_model: str | None) -> list[str]:
        if preferred_model:
            primary = normalize_model_name(preferred_model)
        else:
            primary = get_default_model()
        return [primary, *get_model_fallbacks(primary)]
