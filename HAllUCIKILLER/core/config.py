"""
Configuration settings for Hallucikiller.
"""

import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    app_name: str = "Hallucikiller AI Safety Evaluation Pipeline"
    app_version: str = "2027.1.0"
    api_host: str = os.getenv("HALLUCIKILLER_API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("HALLUCIKILLER_API_PORT", "8000"))
    default_judge_model: str = os.getenv("HALLUCIKILLER_JUDGE_MODEL", "mock-gpt-4o-judge")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openrouter_api_key: str = os.getenv("OPENROUTER_API_KEY", "")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    hf_token: str = os.getenv("HUGGINGFACE_API_KEY", "")
    default_pass_threshold_pct: float = 85.0
    default_safety_score_threshold: float = 8.0


settings = Settings()
