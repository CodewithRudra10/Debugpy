
import json
import os

from google import genai

from .base import AIProvider, AnalysisResult


class GeminiProvider(AIProvider):
    """Gemini implementation of the DebugMate AI provider."""

    def __init__(self, model: str):
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set."
            )

        self.client = genai.Client(api_key=self.api_key)
        self.model = model

    def analyze(
        self,
        error_type: str,
        error_message: str,
        source_code: str,
        instructions: str,
    ) -> AnalysisResult:
        prompt = f"""
You are DebugMate, a Python debugging assistant.

Analyze the error using the information below.

Error type: {error_type}
Error message: {error_message}
Source code:
{source_code}

Instructions:
{instructions}

Return ONLY a valid JSON object with these four string fields:
- error_type
- cause
- suggested_fix
- explanation

Do not execute code or claim that a suggested fix has been tested.
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0.2,
            },
        )

        if not response.text:
            raise ValueError("Gemini returned an empty response.")

        try:
            result = json.loads(response.text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Gemini returned an invalid JSON diagnosis."
            ) from exc

        required_fields = {
            "error_type",
            "cause",
            "suggested_fix",
            "explanation",
        }

        if not isinstance(result, dict) or not required_fields.issubset(result):
            raise ValueError(
                "Gemini's response is missing required diagnosis fields."
            )

        if not all(
            isinstance(result[field], str)
            for field in required_fields
        ):
            raise ValueError(
                "All diagnosis fields must contain strings."
            )

        return AnalysisResult(
            error_type=result["error_type"],
            cause=result["cause"],
            suggested_fix=result["suggested_fix"],
            explanation=result["explanation"],
        )
