"""
Ollama Target Adapter.
Connects directly to local Ollama API instances.
"""

import time
import httpx
from typing import Tuple, Optional
from core.adapters.base import BaseTargetAdapter
from core.models import ModelConfig


class OllamaTargetAdapter(BaseTargetAdapter):
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        base = config.endpoint_url or "http://localhost:11434"
        if not base.endswith("/api/generate") and not base.endswith("/api/chat"):
            self.endpoint_url = f"{base.rstrip('/')}/api/generate"
        else:
            self.endpoint_url = base

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> Tuple[str, float]:
        payload = {
            "model": self.config.model_name or "llama3",
            "prompt": prompt,
            "system": system_prompt or "",
            "stream": False,
            "options": {
                "temperature": self.config.temperature,
                "num_predict": self.config.max_tokens
            }
        }

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
            try:
                response = await client.post(self.endpoint_url, json=payload)
                response.raise_for_status()
                data = response.json()
                text = data.get("response", "")
            except Exception as e:
                text = f"[Ollama Adapter Error]: {str(e)}"

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return text, round(latency_ms, 2)
