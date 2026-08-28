from __future__ import annotations
import os
from typing import Optional


class Settings:
    """Centralized deployment settings and API key management for AI Career Engine."""

    # Primary AI / LLM Provider Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-2.5-flash")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-004")


    # Optional Alternative LLM Provider (OpenAI Fallback)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Live Job Market Data API Keys (Optional for real-time market ingestion)
    ADZUNA_APP_ID: Optional[str] = os.getenv("ADZUNA_APP_ID")
    ADZUNA_APP_KEY: Optional[str] = os.getenv("ADZUNA_APP_KEY")
    JOOBLE_API_KEY: Optional[str] = os.getenv("JOOBLE_API_KEY")

    # Deployment Environment Config
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def get_active_llm_key(cls) -> Optional[str]:
        """Returns the primary active LLM API key."""
        return cls.GEMINI_API_KEY or cls.OPENAI_API_KEY


settings = Settings()
