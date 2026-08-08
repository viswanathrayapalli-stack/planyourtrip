from app.ai.providers.ai_provider import AIProvider
from app.core.settings import settings


class OpenAIProvider(AIProvider):
    """OpenAI implementation of AIProvider."""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    def generate(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError