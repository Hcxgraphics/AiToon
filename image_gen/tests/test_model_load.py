from __future__ import annotations

from image_gen.api.pixazo_client import extract_image_url
from image_gen.core.config import PIXAZO_MODELS, normalize_model_name


if __name__ == "__main__":
    assert normalize_model_name("flux-schnell") == "flux"
    assert normalize_model_name("sdxl-lightning") == "lightning"
    assert normalize_model_name("sdxl") == "sdxl"
    assert "flux" in PIXAZO_MODELS
    assert extract_image_url("flux", {"output": "https://example.com/image.png"}) == "https://example.com/image.png"
    print("Model routing and Pixazo response parsing checks passed.")
