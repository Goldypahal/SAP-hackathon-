from __future__ import annotations
import unittest
from engines import SkillGapEngine, MatchingEngine, ReadinessEngine, SkillEngine
from engines.matching_engine import calculate_effective_experience


class TestRegressionEdgeCases(unittest.TestCase):
    """Regression test suite for edge cases, protected gaps, missing flags, duplicate skills, boundary values, and score bounds."""

    def setUp(self):
        self.skill_engine = SkillEngine()
        self.gap_engine = SkillGapEngine(self.skill_engine)
        self.matching_engine = MatchingEngine(self.skill_engine)
        self.readiness_engine = ReadinessEngine(self.skill_engine)

    def test_calculate_effective_experience_strict_protected_check(self):
        # 1. Protected = True -> Experience restored
        exp_protected = calculate_effective_experience(2.0, [{"duration_months": 12, "protected": True}])
        self.assertEqual(exp_protected, 3.0)

        # 2. Protected = False -> Experience NOT restored
        exp_unprotected = calculate_effective_experience(2.0, [{"duration_months": 12, "protected": False}])
        self.assertEqual(exp_unprotected, 2.0)

        # 3. Protected field missing -> Experience NOT restored (Fixes g.get("protected", True) bug)
        exp_missing = calculate_effective_experience(2.0, [{"duration_months": 12}])
        self.assertEqual(exp_missing, 2.0)

    def test_proficiency_clamping_prevents_score_inflation(self):
        candidate = {
            "name": "Inflated Skill Candidate",
            "experience_years": 3.0,
            "education": ["Bachelor"],
            "location": "Remote",
            "skills": [
                {"name": "Python", "proficiency": 5.0}, # Out of bounds > 1.0
                {"name": "SQL", "proficiency": -2.0},   # Out of bounds < 0.0
            ]
        }
        target_role = {
            "name": "Data Analyst",
            "required_skills": [{"name": "Python", "proficiency": 0.8}, {"name": "SQL", "proficiency": 0.5}],
            "experience_min": 2.0,
        }

        readiness = self.readiness_engine.calculate(candidate, target_role)
        self.assertGreaterEqual(readiness["readiness_score"], 0)
        self.assertLessEqual(readiness["readiness_score"], 100)

        gaps = self.gap_engine.analyze(candidate["skills"], target_role["required_skills"])
        for g in gaps:
            self.assertGreaterEqual(g["current_level"], 0.0)
            self.assertLessEqual(g["current_level"], 1.0)
            self.assertGreaterEqual(g["required_level"], 0.0)
            self.assertLessEqual(g["required_level"], 1.0)

    def test_duplicate_skills_handling(self):
        candidate_skills = [
            {"name": "Python", "normalized_name": "python", "proficiency": 0.4},
            {"name": "python", "normalized_name": "python", "proficiency": 0.8}, # Duplicate normalized name
        ]
        processed = self.skill_engine.process_candidate_skills(candidate_skills)
        self.assertEqual(len(processed), 2)
        for p in processed:
            self.assertEqual(p.normalized_name, "python")


    def test_skill_gap_priority_boundaries(self):
        candidate_skills = [{"name": "Docker", "proficiency": 0.3}]
        required_skills = [{"name": "Docker", "proficiency": 0.8}]
        gaps = self.gap_engine.analyze(candidate_skills, required_skills, candidate_experience_years=1.0)
        
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["gap"], 0.5)
        self.assertEqual(gaps[0]["priority"], "high")

    def test_opportunity_ranking_order_invariants(self):
        candidate = {
            "skills": [{"name": "Python", "proficiency": 0.9}, {"name": "SQL", "proficiency": 0.8}],
            "experience_years": 5.0,
            "education": ["Bachelor of Science"],
            "location": "Remote",
        }
        opportunities = [
            {"title": "Low Match", "required_skills": ["C++", "Rust"], "experience_min": 10.0, "location": "Onsite"},
            {"title": "High Match", "required_skills": ["Python", "SQL"], "experience_min": 3.0, "location": "Remote"},
        ]

        ranked = self.matching_engine.rank(candidate, opportunities)
        self.assertEqual(ranked[0]["title"], "High Match")
        self.assertGreater(ranked[0]["compatibility_score"], ranked[1]["compatibility_score"])


if __name__ == "__main__":
    unittest.main()
