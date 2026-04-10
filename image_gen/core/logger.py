from __future__ import annotations

import logging
import sys

from image_gen.core.config import BATCH_CONFIG

LOGGER_NAME = "aitoon.image_pipeline"


def get_logger(name: str | None = None) -> logging.Logger:
    logger = logging.getLogger(name or LOGGER_NAME)
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG if BATCH_CONFIG.enable_debug_logs else logging.INFO)
    logger.propagate = False
    return logger
