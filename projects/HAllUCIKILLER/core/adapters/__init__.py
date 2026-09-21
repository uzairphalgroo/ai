"""
Target Adapter Factory.
"""

from core.models import ModelConfig, TargetProvider
from core.adapters.base import BaseTargetAdapter
from core.adapters.mock_engine import MockTargetAdapter
from core.adapters.openai_adapter import OpenAICompatibleAdapter
from core.adapters.ollama_adapter import OllamaTargetAdapter
from core.adapters.huggingface_adapter import HuggingFaceTargetAdapter
from core.adapters.openrouter_adapter import OpenRouterTargetAdapter


def get_target_adapter(config: ModelConfig) -> BaseTargetAdapter:
    if config.provider == TargetProvider.MOCK:
        return MockTargetAdapter(config)
    elif config.provider == TargetProvider.OPENROUTER:
        return OpenRouterTargetAdapter(config)
    elif config.provider == TargetProvider.OPENAI:
        return OpenAICompatibleAdapter(config)
    elif config.provider == TargetProvider.OLLAMA:
        return OllamaTargetAdapter(config)
    elif config.provider == TargetProvider.HUGGINGFACE:
        return HuggingFaceTargetAdapter(config)
    else:
        return MockTargetAdapter(config)
