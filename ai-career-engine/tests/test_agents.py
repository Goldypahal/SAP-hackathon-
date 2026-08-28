from __future__ import annotations
import json
import os
import unittest

from models import CandidateProfile, TargetRole, Skill
from engines import SkillGapEngine, MatchingEngine, ReadinessEngine
from agents import (
    SkillAnalysisAgent,
    CareerResearchAgent,
    LearningAgent,
    OpportunityAgent,
    IndustryIntelligenceAgent,
    ProfileIntelligenceAgent,
)
from orchestrator import AgentOrchestrator


class TestAICareerEngine(unittest.TestCase):

    def setUp(self):
        sample_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "examples",
            "sample_candidate.json",
        )
        with open(sample_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def test_schemas(self):
        cand = CandidateProfile.model_validate(self.data["candidate"])
        role = TargetRole.model_validate(self.data["target_role"])
        self.assertEqual(cand.name, "Alex Mercer")
        self.assertEqual(role.name, "ML Engineer")
        self.assertTrue(cand.career_gaps[0].protected)

    def test_skill_gap_engine(self):
        engine = SkillGapEngine()
        cand_skills = self.data["candidate"]["skills"]
        req_skills = self.data["target_role"]["required_skills"]
        gaps = engine.analyze(cand_skills, req_skills)
        
        gap_names = [g["skill"].lower() for g in gaps]
        self.assertIn("docker", gap_names)
        self.assertIn("kubernetes", gap_names)
        self.assertIn("mlops", gap_names)
        
        # Verify Docker priority is high
        docker_gap = next(g for g in gaps if g["skill"].lower() == "docker")
        self.assertEqual(docker_gap["priority"], "high")

    def test_matching_engine_protected_gaps(self):
        engine = MatchingEngine()
        cand_data = {
            "skills": ["Python", "SQL", "Pandas"],
            "education": ["Bachelor"],
            "experience_years": 2.5,
            "location": "Remote",
            "career_gaps": [{"reason": "Family Care", "protected": True}],
        }
        opps = [
            {
                "title": "ML Engineer",
                "company": "TechCorp",
                "required_skills": ["Python", "SQL", "Pandas", "Docker"],
                "preferred_skills": [],
                "experience_required": 2.0,
                "education_required": "Bachelor",
                "location": "Remote",
            }
        ]
        ranked = engine.rank(cand_data, opps)
        self.assertEqual(len(ranked), 1)
        self.assertGreaterEqual(ranked[0]["compatibility_score"], 80)
        self.assertIn("Python", ranked[0]["why_matched"])
        self.assertIn("Docker", ranked[0]["gaps"])

    def test_orchestrator_pipeline(self):
        orchestrator = AgentOrchestrator()
        result_state = orchestrator.run_career_pipeline(self.data)

        self.assertIn("strengths", result_state)
        self.assertIn("skill_gaps", result_state)
        self.assertIn("learning_plan", result_state)
        self.assertIn("matched_opportunities", result_state)
        self.assertIn("readiness", result_state)
        self.assertIn("roadmap", result_state)


if __name__ == "__main__":
    unittest.main()
