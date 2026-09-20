"""
Base target adapter interface.
"""

from abc import ABC, abstractmethod
from typing import Tuple
from core.models import ModelConfig


class BaseTargetAdapter(ABC):
    def __init__(self, config: ModelConfig):
        self.config = config

    @abstractmethod
    async def generate_response(self, prompt: str, system_prompt: str = None) -> Tuple[str, float]:
        """
        Generate response from the target model.
        Returns:
            Tuple[str, float]: (model_response_text, latency_ms)
        """
        pass
