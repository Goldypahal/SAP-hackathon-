from __future__ import annotations
import unittest
from unittest.mock import patch, MagicMock
from llm.provider import LLMProvider
from agents import (
    SkillAnalysisAgent,
    CareerResearchAgent,
    IndustryIntelligenceAgent,
    LearningAgent,
    OpportunityAgent,
    ProfileIntelligenceAgent,
)


class TestLLMProvider(unittest.TestCase):
    """Test LLMProvider initialization, provider routing, and fallbacks."""

    def test_provider_initialization_defaults(self):
        provider = LLMProvider()
        self.assertIsNotNone(provider.provider)
        self.assertIsNotNone(provider.model_name)

    def test_simulation_fallback_when_no_api_key(self):
        provider = LLMProvider(provider="gemini")
        explanation = provider.generate_explanation("Analyze Python skills", "System Prompt")
        self.assertTrue(len(explanation) > 0)
        self.assertIn("Gemini", explanation)

    @patch("urllib.request.urlopen")
    def test_gemini_rest_api_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"candidates": [{"content": {"parts": [{"text": "Gemini AI explanation result."}]}}]}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        with patch("config.settings.settings.GEMINI_API_KEY", "test_gemini_key"):
            provider = LLMProvider(provider="gemini")
            res = provider.generate_explanation("Test prompt", "Test instruction")
            self.assertEqual(res, "Gemini AI explanation result.")

    @patch("urllib.request.urlopen")
    def test_openai_rest_api_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"choices": [{"message": {"content": "OpenAI explanation result."}}]}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response

        with patch("config.settings.settings.OPENAI_API_KEY", "test_openai_key"):
            provider = LLMProvider(provider="openai")
            res = provider.generate_explanation("Test prompt", "Test instruction")
            self.assertEqual(res, "OpenAI explanation result.")


class TestAgentLLMIntegration(unittest.TestCase):
    """Test LLM explanation output in agent results."""

    def setUp(self):
        self.sample_context = {
            "candidate": {
                "candidate_id": "cand_12345",
                "name": "Jane Doe",
                "current_role": "Data Analyst",
                "experience_years": 3.0,
                "skills": [{"name": "Python", "normalized_name": "python", "proficiency": 0.8, "recency": "current"}],
                "projects": [],
                "courses_completed": [],
                "education": ["Bachelor of Science"],
                "location": "Remote",
                "career_gaps": [],
            },
            "target_role": {
                "name": "Data Scientist",
                "required_skills": [{"name": "Python", "normalized_name": "python", "proficiency": 0.9}],
                "preferred_skills": [],
            },
            "jobs": [],
        }


    def test_skill_analysis_agent_llm_output(self):
        agent = SkillAnalysisAgent()
        result = agent.execute(self.sample_context)
        self.assertEqual(result.status, "success")
        self.assertIn("explanation", result.data)
        self.assertTrue(len(result.data["explanation"]) > 0)

    def test_career_research_agent_llm_output(self):
        agent = CareerResearchAgent()
        result = agent.execute(self.sample_context)
        self.assertEqual(result.status, "success")
        self.assertIn("explanation", result.data)

    def test_industry_intelligence_agent_llm_output(self):
        agent = IndustryIntelligenceAgent()
        result = agent.execute(self.sample_context)
        self.assertEqual(result.status, "success")
        self.assertIn("explanation", result.data)

    def test_learning_agent_llm_output(self):
        agent = LearningAgent()
        result = agent.execute(self.sample_context)
        self.assertEqual(result.status, "success")
        self.assertIn("explanation", result.data)

    def test_opportunity_agent_llm_output(self):
        agent = OpportunityAgent()
        result = agent.execute(self.sample_context)
        self.assertEqual(result.status, "success")
        self.assertIn("explanation", result.data)

    def test_profile_intelligence_agent_llm_output(self):
        agent = ProfileIntelligenceAgent()
        result = agent.execute(self.sample_context)
        self.assertEqual(result.status, "success")
        self.assertIn("explanation", result.data)


if __name__ == "__main__":
    unittest.main()
