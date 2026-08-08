from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Abstraction for AI providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        raise NotImplementedError