from app.ai.prompts import build_itinerary_prompt
from app.ai.providers import AIProvider


class ItineraryAIService:

    def __init__(
        self,
        provider: AIProvider,
    ):
        self.provider = provider

    def generate_itinerary(
        self,
        destination: str,
        start_date: str,
        end_date: str,
        budget: str,
        travelers: int,
    ) -> str:
        prompt = build_itinerary_prompt(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            budget=budget,
            travelers=travelers,
        )
        return self.provider.generate(prompt)
