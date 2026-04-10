from __future__ import annotations

from io import BytesIO
from typing import Optional

import requests
from PIL import Image, UnidentifiedImageError

from image_gen.core.config import (
    BATCH_CONFIG,
    get_model_config,
    get_request_headers,
    normalize_model_name,
)
from image_gen.core.logger import get_logger

logger = get_logger(__name__)


def extract_image_url(model_name: str, response_json: dict) -> str:
    key_map = {
        "sdxl": "imageUrl",
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
            "height": model_config.default_height,
            "width": model_config.default_width,
            "num_steps": model_config.default_steps,
            "guidance_scale": model_config.default_guidance_scale,
            "seed": model_config.default_seed if seed is None else seed,
        }

        logger.info("Submitting Pixazo request for model=%s", normalized_model)
        response = self.session.post(
            model_config.endpoint,
            headers=get_request_headers(),
            json=payload,
            timeout=BATCH_CONFIG.request_timeout_seconds,
        )
        image = self._parse_response_image(response=response, model_name=normalized_model)
        return image

    def _parse_response_image(self, response: requests.Response, model_name: str) -> Image.Image:
        response.raise_for_status()
        content_type = response.headers.get("Content-Type", "").lower()

        if content_type.startswith("image/"):
            return self._decode_image_bytes(response.content, model_name, content_type)

        response_json = response.json()
        image_url = extract_image_url(model_name, response_json)
        image_response = self.session.get(image_url, timeout=BATCH_CONFIG.request_timeout_seconds)
        image_response.raise_for_status()
        return self._decode_image_bytes(
            image_response.content,
            model_name=model_name,
            content_type=image_response.headers.get("Content-Type"),
        )

    @staticmethod
    def _decode_image_bytes(content: bytes, model_name: str, content_type: str | None) -> Image.Image:
        if len(content) < 1000:
            raise ValueError("Downloaded content too small to be a valid image payload.")
        try:
            image = Image.open(BytesIO(content))
            return image.convert("RGB")
        except UnidentifiedImageError as exc:
            raise ValueError(
                f"Unable to decode image bytes for model '{model_name}'. Content-Type was {content_type}"
            ) from exc
