from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from dotenv import load_dotenv

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PACKAGE_ROOT.parent
SERVER_ROOT = REPO_ROOT / "server"
ENV_FILE = PACKAGE_ROOT / ".env.image_gen"

load_dotenv(ENV_FILE, override=False)

if str(SERVER_ROOT) not in sys.path:
    sys.path.insert(0, str(SERVER_ROOT))

OUTPUT_DIR = (PACKAGE_ROOT / os.getenv("OUTPUT_DIR", "outputs/panels")).resolve()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class APIModelConfig:
    name: str
    endpoint: str
    quality_tier: str
    intended_use: str
    default_steps: int
    default_guidance_scale: float


@dataclass(frozen=True)
class BatchConfig:
    max_workers: int
    request_timeout_seconds: int
    max_retries: int
    retry_backoff_seconds: float
    enable_debug_logs: bool


PIXAZO_API_KEY = os.getenv("AITOON_PIXAZO_API_KEY", "")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "lightning")
DEFAULT_IMAGE_SIZE: Tuple[int, int] = (
    int(os.getenv("AITOON_DEFAULT_WIDTH", "1024")),
    int(os.getenv("AITOON_DEFAULT_HEIGHT", "1024")),
)
DEFAULT_NEGATIVE_PROMPT = (
    "blurry, low quality, distorted anatomy, duplicate limbs, watermark, text artifacts, "
    "cropped face, extra fingers, malformed hands, bad composition"
)

PIXAZO_MODELS: Dict[str, APIModelConfig] = {
    "flux": APIModelConfig(
        name="flux",
        endpoint="https://gateway.pixazo.ai/flux-1-schnell/v1/getData",
        quality_tier="draft",
        intended_use="Fast storyboard drafts and low-complexity preview scenes.",
        default_steps=8,
        default_guidance_scale=3.5,
    ),
    "sdxl": APIModelConfig(
        name="sdxl",
        endpoint="https://gateway.pixazo.ai/getImage/v1/getSDXLImage",
        quality_tier="final",
        intended_use="High-quality render path for important and emotional scenes.",
        default_steps=28,
        default_guidance_scale=7.0,
    ),
    "lightning": APIModelConfig(
        name="lightning",
        endpoint="https://gateway.pixazo.ai/sdxl_lightning/getImage/v1/getSDXLImage",
        quality_tier="refined-fast",
        intended_use="Fast refined renders for multi-character or medium-complexity scenes.",
        default_steps=12,
        default_guidance_scale=4.5,
    ),
}

MODEL_FALLBACK_ORDER: Dict[str, Tuple[str, ...]] = {
    "flux": ("lightning", "sdxl"),
    "lightning": ("sdxl", "flux"),
    "sdxl": ("lightning", "flux"),
}

MODEL_ALIASES: Dict[str, str] = {
    "flux": "flux",
    "flux-schnell": "flux",
    "lightning": "lightning",
    "sdxl-lightning": "lightning",
    "sdxl": "sdxl",
    "sdxl-base": "sdxl",
}

THEME_STYLE_MAP: Dict[str, str] = {
    "anime": "anime style",
    "fantasy": "fantasy anime style",
    "cyberpunk": "cyberpunk anime style",
    "noir": "noir graphic anime style",
    "cartoon": "stylized cartoon-comic style",
}

BATCH_CONFIG = BatchConfig(
    max_workers=max(1, int(os.getenv("MAX_WORKERS", "4"))),
    request_timeout_seconds=int(os.getenv("REQUEST_TIMEOUT", "30")),
    max_retries=int(os.getenv("MAX_RETRIES", "3")),
    retry_backoff_seconds=float(os.getenv("RETRY_BACKOFF_SECONDS", "1.0")),
    enable_debug_logs=os.getenv("ENABLE_DEBUG_LOGS", "True").lower() == "true",
)


def normalize_model_name(model_name: str) -> str:
    normalized = MODEL_ALIASES.get((model_name or "").strip().lower())
    if not normalized:
        raise KeyError(f"Unsupported model name: {model_name}")
    return normalized


def get_output_path(panel_id: int) -> Path:
    return OUTPUT_DIR / f"panel_{panel_id}.png"


def get_model_config(model_name: str) -> APIModelConfig:
    return PIXAZO_MODELS[normalize_model_name(model_name)]


def get_model_fallbacks(model_name: str) -> Tuple[str, ...]:
    return MODEL_FALLBACK_ORDER.get(normalize_model_name(model_name), tuple())


def get_default_model() -> str:
    return normalize_model_name(DEFAULT_MODEL)


def has_pixazo_api_key() -> bool:
    return bool(PIXAZO_API_KEY and PIXAZO_API_KEY != "YOUR_API_KEY")


def get_request_headers() -> Dict[str, str]:
    if not has_pixazo_api_key():
        raise RuntimeError(
            "Missing Pixazo API key. Set AITOON_PIXAZO_API_KEY in image_gen/.env.image_gen before rendering."
        )
    return {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": PIXAZO_API_KEY,
    }
