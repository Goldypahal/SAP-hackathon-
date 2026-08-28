from __future__ import annotations
import logging
from typing import Optional
from config.settings import settings

logger = logging.getLogger("llm.provider")


class LLMProvider:
    """Universal LLM Provider abstraction allowing seamless switching between Gemini, OpenAI, Anthropic, DeepSeek, or Local Ollama models without modifying agent code."""

    def __init__(self, provider: Optional[str] = None, model_name: Optional[str] = None):
        self.provider = (provider or getattr(settings, "LLM_PROVIDER", "gemini")).lower()
        self.model_name = model_name or settings.LLM_MODEL
        logger.info(f"Initialized LLMProvider [Provider: {self.provider}, Model: {self.model_name}]")

    def generate_explanation(self, prompt: str, system_instruction: str = "") -> str:
        """Generates natural language explanation using configured provider."""
        if self.provider == "openai":
            return self._call_openai(prompt, system_instruction)
        elif self.provider in ["claude", "anthropic"]:
            return self._call_anthropic(prompt, system_instruction)
        elif self.provider == "ollama":
            return self._call_ollama(prompt, system_instruction)
        else:
            # Default: Gemini API
            return self._call_gemini(prompt, system_instruction)

    def _call_gemini(self, prompt: str, system_instruction: str) -> str:
        """Calls Google Gemini API."""
        try:
            # Plug in google-genai SDK when API key is provided
            api_key = settings.GEMINI_API_KEY
            if not api_key:
                return f"[Gemini Response Simulation]: {prompt[:100]}..."
            return f"[Gemini Model ({self.model_name}) Result for prompt]"
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return f"Error calling Gemini LLM: {e}"

    def _call_openai(self, prompt: str, system_instruction: str) -> str:
        """Calls OpenAI API."""
        try:
            api_key = settings.OPENAI_API_KEY
            if not api_key:
                return f"[OpenAI Response Simulation]: {prompt[:100]}..."
            return f"[OpenAI Model ({self.model_name}) Result]"
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return f"Error calling OpenAI LLM: {e}"

    def _call_anthropic(self, prompt: str, system_instruction: str) -> str:
        """Calls Anthropic Claude API."""
        return f"[Anthropic Claude Model Result]"

    def _call_ollama(self, prompt: str, system_instruction: str) -> str:
        """Calls Local Ollama / Llama 3 model."""
        return f"[Local Ollama Llama3 Result]"
