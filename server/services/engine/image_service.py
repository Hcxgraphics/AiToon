from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List

CURRENT_FILE = Path(__file__).resolve()
APP_ROOT = CURRENT_FILE.parents[3]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from image_gen.pipeline.batch_renderer import BatchRenderer


class ImageGenerationService:
    """Bridge layer between the backend service layer and the shared image_gen engine."""

    def __init__(self, renderer: BatchRenderer | None = None):
        self.renderer = renderer or BatchRenderer()

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
