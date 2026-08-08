from openai import APIError, AuthenticationError, OpenAI

from app.ai.constants import AI_DISABLED
from app.ai.providers.ai_provider import AIProvider
from app.core.settings import settings
from app.shared.exceptions.exceptions import ValidationException
from app.shared.logging import get_logger

logger = get_logger(__name__)
class OpenAIProvider(AIProvider):
    """OpenAI implementation of AIProvider."""

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        client_kwargs = {
            "api_key": self.api_key,
            "timeout": 30.0,
        }

        if settings.OPENAI_BASE_URL:
            client_kwargs["base_url"] = settings.OPENAI_BASE_URL

        self.client = OpenAI(**client_kwargs)

    def generate(
        self,
        prompt: str,
    ) -> str:
        if not settings.AI_ENABLED:
            raise ValidationException(AI_DISABLED)

        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt,
            )
        except AuthenticationError as exc:
            raise ValidationException("Invalid OpenAI API key.") from exc
        except APIError as exc:
            logger.exception("OpenAI API request failed.")
            raise ValidationException(
                "OpenAI service is currently unavailable."
            ) from exc

        return response.output_text or ""