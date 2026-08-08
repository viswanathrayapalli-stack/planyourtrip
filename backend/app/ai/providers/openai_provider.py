from openai import OpenAI

from app.ai.providers.ai_provider import AIProvider
from app.core.settings import settings


class OpenAIProvider(AIProvider):
    """OpenAI implementation of AIProvider."""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        client_kwargs = {
            "api_key": self.api_key,
        }

        if settings.OPENAI_BASE_URL:
            client_kwargs["base_url"] = settings.OPENAI_BASE_URL

        self.client = OpenAI(**client_kwargs)

    def generate(
        self,
        prompt: str,
    ) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text or ""