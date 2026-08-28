from __future__ import annotations
from typing import Dict, List, Any
from models.schemas import Skill


class SkillEngine:
    """Deterministic engine to normalize skill names and compute effective skill proficiencies."""

    @staticmethod
    def normalize_skill_name(name: str) -> str:
        """Converts skill names to standard normalized form (lowercased, whitespace trimmed)."""
        if not name:
            return ""
        name = name.strip().lower()
        # Common aliases
        aliases = {
            "py": "python",
            "python3": "python",
            "postgres": "postgresql",
            "ml": "machine learning",
            "k8s": "kubernetes",
            "aws cloud": "aws",
        }
        return aliases.get(name, name)

    def process_candidate_skills(self, skills: List[Dict[str, Any]]) -> List[Skill]:
        """Normalizes and computes overall proficiency for candidate skills."""
        processed: List[Skill] = []
        for s in skills:
            if isinstance(s, dict):
                skill_obj = Skill.model_validate(s)
            else:
                skill_obj = s
            skill_obj.normalized_name = self.normalize_skill_name(skill_obj.name)

            # Recency & project evidence adjustment
            base_prof = skill_obj.proficiency
            if skill_obj.project_evidence > 0:
                base_prof = min(1.0, base_prof + (0.05 * skill_obj.project_evidence))
            if skill_obj.course_completion > 0:
                base_prof = min(1.0, base_prof + (0.05 * skill_obj.course_completion))
            
            effective_prof = round(base_prof * skill_obj.recency_score, 2)
            skill_obj.proficiency = min(1.0, max(0.0, effective_prof))
            processed.append(skill_obj)
        return processed
