from __future__ import annotations

from io import BytesIO
from typing import Optional

import requests
from PIL import Image, UnidentifiedImageError

from image_gen.core.config import BATCH_CONFIG, get_model_config, get_request_headers, normalize_model_name
from image_gen.core.logger import get_logger

logger = get_logger(__name__)


def extract_image_url(model_name: str, response_json: dict) -> str:
    key_map = {
        "sdxl": "imageUrl",
        "lightning": "imageUrl",
        "flux": "output",
    }
    normalized_model = normalize_model_name(model_name)
    response_key = key_map[normalized_model]
    image_url = response_json.get(response_key)
    if not image_url:
        raise ValueError(
            f"Image URL missing in API response for model '{normalized_model}'. "
            f"Expected key '{response_key}', got keys: {sorted(response_json.keys())}"
        )
    return str(image_url)


class PixazoClient:
    """HTTP client for Pixazo-hosted generation models."""

    def __init__(self, session: Optional[requests.Session] = None):
        self.session = session or requests.Session()

    def generate(
        self,
        model_name: str,
        prompt: str,
        negative_prompt: str,
        width: int,
        height: int,
        seed: int,
    ) -> Image.Image:
        normalized_model = normalize_model_name(model_name)
        model_config = get_model_config(normalized_model)
        payload = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "height": height,
            "width": width,
            "num_steps": model_config.default_steps,
            "guidance_scale": model_config.default_guidance_scale,
            "seed": seed,
        }

        logger.info("Submitting Pixazo request for model=%s", normalized_model)
        response = self.session.post(
            model_config.endpoint,
            headers=get_request_headers(),
            json=payload,
            timeout=BATCH_CONFIG.request_timeout_seconds,
        )
        response.raise_for_status()
        response_json = response.json()
        image_url = extract_image_url(normalized_model, response_json)

        image_response = self.session.get(image_url, timeout=BATCH_CONFIG.request_timeout_seconds)
        image_response.raise_for_status()
        if len(image_response.content) < 1000:
            raise ValueError("Downloaded content too small to be a valid image payload.")

        try:
            image = Image.open(BytesIO(image_response.content))
            return image.convert("RGB")
        except UnidentifiedImageError as exc:
            raise ValueError(
                f"Unable to decode image bytes for model '{normalized_model}'. "
                f"Content-Type was {image_response.headers.get('Content-Type')}"
            ) from exc
