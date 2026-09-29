import base64
import json
from typing import Any
from google import genai
from google.genai import types
from ..config import get_settings

class GeminiService:
    def __init__(self):
        self.settings = get_settings()
        self.client = genai.Client(api_key=self.settings.gemini_api_key) if self.settings.gemini_api_key else None

    @property
    def enabled(self) -> bool:
        return self.client is not None

    def generate_json(self, prompt: str, image_bytes: bytes | None = None, mime_type: str | None = None) -> tuple[dict[str, Any] | None, str | None]:
        if not self.client:
            return None, None
        contents: list[Any] = [prompt]
        if image_bytes and mime_type:
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))
        try:
            response = self.client.models.generate_content(
                model=self.settings.gemini_model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3,
                ),
            )
            text = getattr(response, "text", "") or ""
            return json.loads(text), self.settings.gemini_model
        except Exception:
            return None, self.settings.gemini_model
