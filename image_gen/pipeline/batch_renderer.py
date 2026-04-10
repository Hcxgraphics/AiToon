from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Iterable, List, Sequence

from image_gen.core.config import BATCH_CONFIG
from image_gen.core.contracts import RenderArtifact, SceneTask
from image_gen.core.logger import get_logger
from image_gen.pipeline.image_generator import SceneImageGenerator
from image_gen.pipeline.task_splitter import SceneTaskSplitter

logger = get_logger(__name__)


class BatchRenderer:
    """Parallel scene renderer with per-panel fault isolation."""

    def __init__(self, image_generator: SceneImageGenerator | None = None, max_workers: int | None = None):
        self.image_generator = image_generator or SceneImageGenerator()
        self.max_workers = max_workers or BATCH_CONFIG.max_workers
        self.task_splitter = SceneTaskSplitter()

    def render_payload(self, payload: Dict) -> List[RenderArtifact]:
        return self.render_tasks(self.task_splitter.split(payload))

    def render_tasks(self, scene_tasks: Sequence[SceneTask]) -> List[RenderArtifact]:
        if not scene_tasks:
            return []

        results_by_panel: Dict[int, RenderArtifact] = {}
        with ThreadPoolExecutor(max_workers=min(self.max_workers, len(scene_tasks))) as executor:
            future_map = {
                executor.submit(self.image_generator.render, scene): scene.panel_id for scene in scene_tasks
            }
            for future in as_completed(future_map):
                panel_id = future_map[future]
                try:
                    results_by_panel[panel_id] = future.result()
                except Exception as exc:  # noqa: BLE001
                    logger.exception("Unhandled render failure for panel=%s", panel_id)
                    results_by_panel[panel_id] = RenderArtifact(
                        panel_id=panel_id,
                        output_path="",
                        model_used="unassigned",
                        prompt="",
                        fallback_used=False,
                        attempts=0,
                        success=False,
                        error_message=str(exc),
                    )

        ordered_results = [results_by_panel[scene.panel_id] for scene in scene_tasks]
        logger.info(
            "Batch render complete: %s/%s panels succeeded",
            sum(1 for result in ordered_results if result.success),
            len(ordered_results),
        )
        return ordered_results

    def render_panels(self, panels: Iterable[dict], theme: str | None = None) -> List[RenderArtifact]:
        return self.render_payload({"final_output": {"theme": theme, "panels": list(panels)}})

    def render_panel(self, panel: dict, theme: str | None = None) -> RenderArtifact:
        return self.render_panels([panel], theme=theme)[0]
