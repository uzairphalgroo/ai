"""
HuggingFace Target Adapter.
Supports HuggingFace Inference API or local Transformers pipeline.
"""

import time
import httpx
from typing import Tuple, Optional
from core.adapters.base import BaseTargetAdapter
from core.models import ModelConfig


class HuggingFaceTargetAdapter(BaseTargetAdapter):
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.endpoint_url = (
            config.endpoint_url
            or f"https://api-inference.huggingface.co/models/{config.model_name or 'mistralai/Mistral-7B-Instruct-v0.2'}"
        )
        self.api_key = config.api_key or ""

    async def generate_response(self, prompt: str, system_prompt: Optional[str] = None) -> Tuple[str, float]:
        full_prompt = f"System: {system_prompt}\nUser: {prompt}\nAssistant:" if system_prompt else prompt
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": self.config.max_tokens,
                "temperature": max(0.01, self.config.temperature),
                "return_full_text": False
            }
        }

        start_time = time.perf_counter()
        async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
            try:
                response = await client.post(self.endpoint_url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    text = data[0].get("generated_text", "")
                elif isinstance(data, dict):
                    text = data.get("generated_text", str(data))
                else:
                    text = str(data)
            except Exception as e:
                text = f"[HuggingFace Adapter Error]: {str(e)}"

        latency_ms = (time.perf_counter() - start_time) * 1000.0
        return text, round(latency_ms, 2)
