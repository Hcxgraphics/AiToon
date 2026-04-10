from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

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
        image_url: str | None = None,
        mask_url: str | None = None,
    ) -> Dict[str, Any]:
        output_path = APP_ROOT / "image_gen" / "outputs" / "panels" / f"panel_{panel_id}.png"
        saved_path = self.retry_router.inpaint_panel(
            prompt=prompt,
            output_path=str(output_path),
            image_url=image_url,
            mask_url=mask_url,
        )
        return {
            "panel_id": panel_id,
            "output_path": saved_path,
            "model_used": "inpainting",
            "prompt": prompt,
            "fallback_used": False,
            "attempts": 1,
            "success": True,
            "error_message": None,
        }
