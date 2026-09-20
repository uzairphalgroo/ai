"""
OpenRouter Target Adapter for Hallucikiller.
Connects to OpenRouter's API supporting free open-source models:
- meta-llama/llama-3.3-70b-instruct:free
- deepseek/deepseek-r1:free
- google/gemini-2.0-flash-exp:free
- mistralai/mistral-7b-instruct:free
- meta-llama/llama-3.2-3b-instruct:free
"""

import time
import httpx
from typing import Tuple, Optional
from core.adapters.base import BaseTargetAdapter
from core.models import ModelConfig
from core.config import settings


class OpenRouterTargetAdapter(BaseTargetAdapter):
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.endpoint_url = config.endpoint_url or "https://openrouter.ai/api/v1/chat/completions"
        self.api_key = config.api_key or settings.openrouter_api_key or ""

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> Tuple[str, float]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "https://hallucikiller.vercel.app",
            "X-Title": "HalluciKiller Tactical AI Defense Matrix"
        }

        model_name = self.config.model_name
        if not model_name or model_name.startswith("mock"):
            model_name = "meta-llama/llama-3.3-70b-instruct:free"

        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
            try:
                response = await client.post(self.endpoint_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                text = data["choices"][0]["message"]["content"]
            except Exception as e:
                text = f"[OpenRouter Adapter Error]: {str(e)}"

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return text, round(latency_ms, 2)
