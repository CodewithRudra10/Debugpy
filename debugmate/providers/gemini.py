"""Gemini provider implementation for Debugmate."""

from __future__ import annotations

from typing import Any, Optional

from .base import BaseProvider


class GeminiProvider(BaseProvider):
    """Concrete provider for Google's Gemini models."""

    api_key_env_var = "GEMINI_API_KEY"
    default_model = "gemini-1.5-flash"

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(api_key=api_key, model=model, **kwargs)

    def _ensure_client(self):
        if self.client is not None:
            return self.client

        try:
            import google.generativeai as genai
        except ImportError as exc:  # pragma: no cover - depends on optional dependency.
            raise ImportError(
                "google-generativeai is required to use GeminiProvider. "
                "Install it with `pip install google-generativeai`."
            ) from exc

        if not self.api_key:
            raise ValueError(
                "A Gemini API key is required. Set GEMINI_API_KEY or pass api_key=..."
            )

        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(self.model)
        return self.client

    def generate(self, prompt: str, **kwargs: Any) -> str:
        client = self._ensure_client()

        request_kwargs = dict(self.config)
        request_kwargs.update(kwargs)

        generation_config = request_kwargs.pop("generation_config", None)
        safety_settings = request_kwargs.pop("safety_settings", None)

        if generation_config is not None or safety_settings is not None:
            response = client.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
                **request_kwargs,
            )
        else:
            response = client.generate_content(prompt, **request_kwargs)

        return self._extract_text(response)

    def stream(self, prompt: str, **kwargs: Any):
        client = self._ensure_client()
        request_kwargs = dict(self.config)
        request_kwargs.update(kwargs)
        return client.generate_content(prompt, stream=True, **request_kwargs)

    @staticmethod
    def _extract_text(response: Any) -> str:
        if hasattr(response, "text"):
            return response.text
        return str(response)
