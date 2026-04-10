from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

CURRENT_FILE = Path(__file__).resolve()
APP_ROOT = CURRENT_FILE.parents[3]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from image_gen.api.retry_fallback_router import RetryFallbackRouter
from image_gen.pipeline.batch_renderer import BatchRenderer


class ImageGenerationService:
    """Bridge layer between the backend service layer and the shared image_gen engine."""

    def __init__(
        self,
        renderer: BatchRenderer | None = None,
        retry_router: RetryFallbackRouter | None = None,
    ):
        self.renderer = renderer or BatchRenderer()
        self.retry_router = retry_router or RetryFallbackRouter()

    def generate_panels(self, orchestrator_output: Dict[str, Any]) -> List[Dict[str, Any]]:
        artifacts = self.renderer.render_payload(orchestrator_output)
        return [
            {
                "panel_id": artifact.panel_id,
                "output_path": artifact.output_path,
                "model_used": artifact.model_used,
                "prompt": artifact.prompt,
                "fallback_used": artifact.fallback_used,
                "attempts": artifact.attempts,
                "success": artifact.success,
                "error_message": artifact.error_message,
            }
            for artifact in artifacts
        ]

    def regenerate_panel(
        self,
        *,
        panel_id: int,
        prompt: str,
        preferred_model: Optional[str] = None,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: int = 42,
    ) -> Dict[str, Any]:
        output_path = APP_ROOT / "image_gen" / "outputs" / "panels" / f"panel_{panel_id}.png"
        execution = self.retry_router.regenerate_with_retry(
            panel_id=panel_id,
            prompt=prompt,
            output_path=str(output_path),
            preferred_model=preferred_model,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            seed=seed,
        )
        return {
            "panel_id": panel_id,
            "output_path": execution.output_path,
            "model_used": execution.model_used,
            "prompt": prompt,
            "fallback_used": execution.fallback_used,
            "attempts": execution.attempts,
            "success": True,
            "error_message": None,
        }
