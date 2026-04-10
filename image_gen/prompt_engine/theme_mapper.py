from __future__ import annotations

from image_gen.core.config import THEME_STYLE_MAP


def normalize_theme(theme: str) -> str:
    cleaned = (theme or "Anime").strip()
    return cleaned[:1].upper() + cleaned[1:] if cleaned else "Anime"


def get_theme_style(theme: str) -> str:
    return THEME_STYLE_MAP.get((theme or "").strip().lower(), THEME_STYLE_MAP["anime"])
