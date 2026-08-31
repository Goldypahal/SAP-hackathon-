from __future__ import annotations
import unittest
from llm.provider import LLMProvider


class TestNvidiaLLMLive(unittest.TestCase):
    """Live E2E test suite calling real NVIDIA Nemotron API endpoints on demand."""

    def test_live_nemotron_completion(self):
        provider = LLMProvider(provider="nemotron", model_name="nvidia/nemotron-3-ultra-550b-a55b")
        response = provider.generate_explanation(
            prompt="Briefly state one key career development advice in 1 sentence.",
            system_instruction="You are an AI Career Coach."
        )
        self.assertIsNotNone(response)
        self.assertGreater(len(response), 10)
        self.assertNotIn("Simulation Mode", response)


if __name__ == "__main__":
    unittest.main()
