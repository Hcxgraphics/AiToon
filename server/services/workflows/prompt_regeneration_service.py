from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional
from urllib import error, request

from dotenv import load_dotenv
from orchestrator.logger import get_logger

CURRENT_FILE = Path(__file__).resolve()
APP_ROOT = CURRENT_FILE.parents[3]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from image_gen.db.prompt_history_store import PromptHistoryStore

load_dotenv()

logger = get_logger("services.workflows.prompt_regeneration")

PROMPT_FUSION_SYSTEM_PROMPT = (
    "You are Prompt Fusion Optimizer for the AiToon backend. "
    "Combine the original panel prompt and the regeneration instruction. "
    "Preserve character consistency, anchor tokens, scene continuity, and camera framing. "
    "Give more weight to the regeneration instruction. "
    "Treat the original context as 40% priority and the regeneration instruction as 60% priority. "
    "Return only the final optimized image-generation prompt."
)


class PromptRegenerationService:
    """Builds optimized regeneration prompts from prompt history and new instructions."""

    def __init__(self, prompt_history_store: PromptHistoryStore | None = None):
        self.prompt_history_store = prompt_history_store or PromptHistoryStore()

    def build_regeneration_prompt(self, panel_id: int, regeneration_instruction: str) -> str:
        history = self.prompt_history_store.fetch_prompt_history(panel_id)
        if not history:
            logger.warning("No prompt history found for panel=%s; using raw regeneration instruction", panel_id)
            return regeneration_instruction.strip()

        fusion_prompt = self._build_fusion_prompt(
            history=history,
            regeneration_instruction=regeneration_instruction,
        )
        return self._generate_fused_prompt(fusion_prompt).strip()

    @staticmethod
    def _build_fusion_prompt(history: Dict[str, Any], regeneration_instruction: str) -> str:
        scene_metadata = json.dumps(history.get("scene_metadata", {}), ensure_ascii=False)
        prompt_versions = history.get("prompt_versions", [])[-5:]
        prompt_versions_text = "\n".join(f"- {item}" for item in prompt_versions) or "- None"
        anchor_tokens = ", ".join(history.get("character_anchor_tokens", [])) or "None"
        return (
            f"Original panel prompt:\n{history.get('final_render_prompt') or history.get('original_prompt', '')}\n\n"
            f"Original prompt baseline:\n{history.get('original_prompt', '')}\n\n"
            f"Character anchor tokens:\n{anchor_tokens}\n\n"
            f"Scene metadata:\n{scene_metadata}\n\n"
            f"Prior prompt history:\n{prompt_versions_text}\n\n"
            f"Regeneration instruction:\n{regeneration_instruction.strip()}\n"
        )

    def _generate_fused_prompt(self, prompt: str) -> str:
        generators = [
            self._generate_with_groq,
            self._generate_with_gemini,
            self._generate_with_openrouter,
        ]
        last_error: Optional[Exception] = None
        for generator in generators:
            try:
                raw_output = generator(prompt)
                return self._sanitize_fused_prompt(raw_output)
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                logger.warning("Prompt fusion provider failed: %s", exc)
        raise RuntimeError(f"All prompt fusion providers failed: {last_error}")

    def _generate_with_groq(self, prompt: str) -> str:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is not configured.")
        from groq import Groq

        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"),
            temperature=0.2,
            max_tokens=400,
            messages=[
                {"role": "system", "content": PROMPT_FUSION_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()

    def _generate_with_gemini(self, prompt: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured.")
        from google import genai

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 400,
                "system_instruction": PROMPT_FUSION_SYSTEM_PROMPT,
            },
        )
        text = getattr(response, "text", None)
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("Gemini prompt fusion returned no text.")
        return text.strip()

    def _generate_with_openrouter(self, prompt: str) -> str:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not configured.")
        payload = {
            "model": os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini"),
            "messages": [
                {"role": "system", "content": PROMPT_FUSION_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 400,
        }
        req = request.Request(
            os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions"),
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", "https://aitoon.local"),
                "X-Title": os.getenv("OPENROUTER_APP_TITLE", "AiToon"),
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"OpenRouter request failed: {exc.code} {body}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"OpenRouter request failed: {exc.reason}") from exc

        try:
            return body["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError("OpenRouter prompt fusion returned an unexpected response.") from exc

    @staticmethod
    def _sanitize_fused_prompt(output: str) -> str:
        cleaned = (output or "").strip()
        if not cleaned:
            raise RuntimeError("Prompt fusion returned empty output.")

        optimized_match = re.search(
            r"optimized prompt:\s*(.+)",
            cleaned,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if optimized_match:
            cleaned = optimized_match.group(1).strip()

        cleaned = re.split(r"\n\s*\n", cleaned, maxsplit=1)[0].strip()
        cleaned = re.sub(r"^['\"`]+|['\"`]+$", "", cleaned).strip()
        cleaned = cleaned.replace("**", "").strip()

        prefixes = (
            "here is the final optimized image-generation prompt:",
            "final optimized prompt:",
            "optimized prompt:",
        )
        lowered = cleaned.lower()
        for prefix in prefixes:
            if lowered.startswith(prefix):
                cleaned = cleaned[len(prefix):].strip()
                break

        if cleaned.lower().startswith("i have incorporated"):
            raise RuntimeError("Prompt fusion output did not contain a usable final prompt.")

        return cleaned
