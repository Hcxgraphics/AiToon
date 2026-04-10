from __future__ import annotations

from typing import Optional

from image_gen.api.retry_fallback_router import RetryFallbackRouter
from image_gen.core.config import BATCH_CONFIG
from image_gen.core.contracts import RenderArtifact, SceneTask
from image_gen.core.logger import get_logger

logger = get_logger(__name__)


class SceneImageGenerator:
    """End-to-end renderer for a single scene task."""

    def __init__(self, retry_router: Optional[RetryFallbackRouter] = None, max_retries: Optional[int] = None):
        self.retry_router = retry_router or RetryFallbackRouter()
        self.max_retries = max_retries or BATCH_CONFIG.max_retries

    def render(self, scene: SceneTask) -> RenderArtifact:
        prompt_package = self.retry_router.build_prompt_package(scene)
        routing = self.retry_router.router.route(scene)
        try:
            execution = self.retry_router.render_with_retry(
                scene_task=scene,
                retries=self.max_retries,
                prompt_package=prompt_package,
            )
            return RenderArtifact(
                panel_id=scene.panel_id,
                output_path=execution.output_path,
                model_used=execution.model_used,
                prompt=prompt_package.positive_prompt,
                fallback_used=execution.fallback_used,
                attempts=execution.attempts,
                success=True,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Render failed for panel=%s", scene.panel_id)
            return RenderArtifact(
                panel_id=scene.panel_id,
                output_path=str(scene.output_path),
                model_used=routing.primary_model,
                prompt=prompt_package.positive_prompt,
                fallback_used=True,
                attempts=self.max_retries,
                success=False,
                error_message=str(exc),
            )
