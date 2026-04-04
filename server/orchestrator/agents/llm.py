import json
import os
import re
import time
from typing import Any, Optional
from urllib import error, request

from orchestrator.agents.utils import parse_json_response
from orchestrator.logger import get_logger
from dotenv import load_dotenv
import os

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

PRIMARY_MODEL = "groq"
SECONDARY_MODEL = "gemini"
FALLBACK_MODEL = "openrouter"

DEFAULT_GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
DEFAULT_OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

STRICT_JSON_SYSTEM_INSTRUCTION = (
    "You are a strict JSON generator for the AiToon orchestrator. "
    "Return only valid JSON with no markdown, no code fences, no commentary, and no trailing text."
)

RATE_LIMIT_RETRY_SECONDS = 35

logger = get_logger("orchestrator.agents.llm")


def _load_windows_user_env(name: str) -> Optional[str]:
    if os.name != "nt":
        return None

    try:
        import winreg
    except ImportError:
        return None

    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
            value, _ = winreg.QueryValueEx(key, name)
    except OSError:
        return None

    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _load_api_key(name: str) -> Optional[str]:
    value = os.getenv(name)
    if value:
        return value
    return _load_windows_user_env(name)


def route_request(task_type):
    if task_type == "fast_agent":
        return PRIMARY_MODEL
    elif task_type == "long_story":
        return SECONDARY_MODEL
    elif task_type == "fallback":
        return FALLBACK_MODEL
    return PRIMARY_MODEL


def _fallback_order(task_type: str) -> list[str]:
    selected = route_request(task_type)

    if selected == PRIMARY_MODEL:
        return [PRIMARY_MODEL, SECONDARY_MODEL, FALLBACK_MODEL]
    if selected == SECONDARY_MODEL:
        return [SECONDARY_MODEL, FALLBACK_MODEL, PRIMARY_MODEL]
    return [FALLBACK_MODEL, SECONDARY_MODEL, PRIMARY_MODEL]


class GroqLLM:
    def __init__(
        self,
        model_name: str = DEFAULT_GROQ_MODEL,
        api_key: Optional[str] = None,
    ) -> None:
        self.model_name = model_name
        self.api_key = api_key or _load_api_key("GROQ_API_KEY")
        self._client: Any = None

    def _load(self) -> None:
        if self._client is not None:
            return

        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is not set. Export GROQ_API_KEY before using Groq.")

        try:
            from groq import Groq
        except ImportError as exc:  # pragma: no cover - depends on environment setup
            raise RuntimeError("groq is not installed. Add it to the environment before using Groq.") from exc

        self._client = Groq(api_key=self.api_key)

    @staticmethod
    def _is_rate_limit_error(exc: Exception) -> bool:
        message = str(exc).lower()
        return "429" in message or "rate limit" in message

    def generate(self, prompt: str, max_new_tokens: int = 1024) -> str:
        self._load()
        response = self._client.chat.completions.create(
            model=self.model_name,
            temperature=0,
            max_tokens=max_new_tokens,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": STRICT_JSON_SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()


class GeminiLLM:
    def __init__(
        self,
        model_name: str = DEFAULT_GEMINI_MODEL,
        api_key: Optional[str] = None,
    ) -> None:
        self.model_name = model_name
        self.api_key = api_key or _load_api_key("GEMINI_API_KEY")
        self._client: Any = None

    def _load(self) -> None:
        if self._client is not None:
            return

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Export GEMINI_API_KEY before using Gemini inference."
            )

        try:
            from google import genai
        except ImportError as exc:  # pragma: no cover - depends on environment setup
            raise RuntimeError(
                "google-genai is not installed. Add it to the environment before using Gemini."
            ) from exc

        self._client = genai.Client(api_key=self.api_key)

    def _build_config(self, max_new_tokens: int) -> dict[str, Any]:
        return {
            "temperature": 0,
            "max_output_tokens": max_new_tokens,
            "response_mime_type": "application/json",
            "system_instruction": STRICT_JSON_SYSTEM_INSTRUCTION,
        }

    def _request_text(self, prompt: str, max_new_tokens: int) -> str:
        try:
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self._build_config(max_new_tokens),
            )
            return self._extract_text(response)
        except Exception as exc:
            if self._is_daily_quota_error(exc):
                raise RuntimeError(
                    "Gemini daily quota is exhausted for the configured model. "
                    "Wait for quota reset, switch to a billed project, or choose a different model."
                ) from exc
            if not self._is_rate_limit_error(exc):
                raise

            delay_seconds = self._retry_delay_seconds(exc)
            logger.warning("Gemini rate limit encountered; retrying in %s seconds", delay_seconds)
            time.sleep(delay_seconds)
            response = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self._build_config(max_new_tokens),
            )
            return self._extract_text(response)

    @staticmethod
    def _is_rate_limit_error(exc: Exception) -> bool:
        message = str(exc)
        return "429" in message and "RESOURCE_EXHAUSTED" in message

    @staticmethod
    def _is_daily_quota_error(exc: Exception) -> bool:
        message = str(exc)
        return "429" in message and ("PerDay" in message or "daily quota" in message.lower())

    @staticmethod
    def _retry_delay_seconds(exc: Exception) -> int:
        match = re.search(r"retry in ([0-9]+(?:\.[0-9]+)?)s", str(exc), flags=re.IGNORECASE)
        if not match:
            return RATE_LIMIT_RETRY_SECONDS
        return max(int(float(match.group(1))) + 1, 1)

    @staticmethod
    def _extract_text(response: Any) -> str:
        text = getattr(response, "text", None)
        if isinstance(text, str) and text.strip():
            return text.strip()

        candidates = getattr(response, "candidates", None) or []
        parts: list[str] = []

        for candidate in candidates:
            content = getattr(candidate, "content", None)
            response_parts = getattr(content, "parts", None) or []

            for part in response_parts:
                part_text = getattr(part, "text", None)
                if isinstance(part_text, str) and part_text.strip():
                    parts.append(part_text.strip())

        if parts:
            return "\n".join(parts).strip()

        raise ValueError("Gemini returned no text content")

    def generate(self, prompt: str, max_new_tokens: int = 1024) -> str:
        self._load()
        response = self._request_text(prompt, max_new_tokens)
        return response.strip()


class OpenRouterLLM:
    def __init__(
        self,
        model_name: str = DEFAULT_OPENROUTER_MODEL,
        api_key: Optional[str] = None,
    ) -> None:
        self.model_name = model_name
        self.api_key = api_key or _load_api_key("OPENROUTER_API_KEY")

    @staticmethod
    def _is_rate_limit_error(exc: Exception) -> bool:
        message = str(exc).lower()
        return "429" in message or "rate limit" in message

    def generate(self, prompt: str, max_new_tokens: int = 1024) -> str:
        if not self.api_key:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set. Export OPENROUTER_API_KEY before using OpenRouter."
            )

        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": STRICT_JSON_SYSTEM_INSTRUCTION},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "max_tokens": max_new_tokens,
            "response_format": {"type": "json_object"},
        }
        req = request.Request(
            OPENROUTER_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
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
            raise ValueError("OpenRouter returned an unexpected response shape") from exc


class RoutedLLM:
    def __init__(self) -> None:
        self.providers = {
            PRIMARY_MODEL: GroqLLM(),
            SECONDARY_MODEL: GeminiLLM(),
            FALLBACK_MODEL: OpenRouterLLM(),
        }

    @staticmethod
    def _is_rate_limit_error(exc: Exception) -> bool:
        message = str(exc).lower()
        return "429" in message or "rate limit" in message or "resource_exhausted" in message

    def _generate_with_repair(
        self,
        provider: Any,
        provider_name: str,
        prompt: str,
        max_new_tokens: int,
    ) -> str:
        attempts = [
            prompt,
            (
                f"{prompt}\n\n"
                "Reminder: return only valid JSON. "
                "Do not include markdown, comments, explanations, or placeholder text."
            ),
        ]
        last_error: Optional[Exception] = None
        raw_text = ""

        for attempt_prompt in attempts:
            raw_text = provider.generate(attempt_prompt, max_new_tokens=max_new_tokens)
            try:
                parsed = parse_json_response(raw_text)
                return json.dumps(parsed, ensure_ascii=False)
            except ValueError as exc:
                last_error = exc
                logger.warning("%s returned invalid JSON; retrying with stricter instruction", provider_name)

        repair_prompt = (
            "Repair the following model output into valid JSON. "
            "Return only the repaired JSON with no commentary.\n\n"
            f"Original task:\n{prompt}\n\n"
            f"Broken output:\n{raw_text}"
        )
        repaired_text = provider.generate(repair_prompt, max_new_tokens=max_new_tokens)
        try:
            parsed = parse_json_response(repaired_text)
            return json.dumps(parsed, ensure_ascii=False)
        except ValueError as exc:
            last_error = exc

        raise ValueError(f"{provider_name} output is not valid JSON after retries: {last_error}")

    def generate(self, prompt: str, max_new_tokens: int = 1024, task_type: str = "fast_agent") -> str:
        fallback_sequence = _fallback_order(task_type)
        last_error: Optional[Exception] = None

        for provider_name in fallback_sequence:
            provider = self.providers[provider_name]
            logger.info("Routing task_type=%s to provider=%s", task_type, provider_name)
            try:
                return self._generate_with_repair(provider, provider_name, prompt, max_new_tokens)
            except Exception as exc:
                last_error = exc
                if self._is_rate_limit_error(exc):
                    logger.warning("%s hit a rate limit; falling back", provider_name)
                else:
                    logger.error("%s failed for task_type=%s: %s", provider_name, task_type, exc)

        raise RuntimeError(f"All model providers failed for task_type='{task_type}': {last_error}")


llm = RoutedLLM()
