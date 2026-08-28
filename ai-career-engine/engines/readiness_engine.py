from __future__ import annotations
from typing import Dict, List, Any


class ReadinessEngine:
    """Deterministic engine to evaluate candidate career readiness score (0-100%)."""

    def calculate(
        self,
        candidate: Dict[str, Any],
        target_role: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Calculates readiness score based on skill overlap, project coverage, and experience."""
        cand_skills = {
            s.get("normalized_name") or s.get("name", "").strip().lower(): float(s.get("proficiency", 0.0))
            for s in candidate.get("skills", [])
        }

        req_skills = target_role.get("required_skills", [])
        if not req_skills:
            skill_score = 1.0
        else:
            total_req = len(req_skills)
            met_sum = 0.0
            for r in req_skills:
                r_name = r.get("normalized_name") or r.get("name", "").strip().lower()
                req_level = float(r.get("proficiency", 0.7))
                curr_level = cand_skills.get(r_name, 0.0)
                if curr_level >= req_level:
                    met_sum += 1.0
                else:
                    met_sum += (curr_level / req_level) if req_level > 0 else 0.0
            skill_score = met_sum / total_req

        # Project score (0-1)
        num_projects = len(candidate.get("projects", []))
        project_score = min(1.0, num_projects * 0.33)

        # Experience score
        cand_exp = candidate.get("experience_years", 0.0)
        target_exp = target_role.get("experience_min", 1.0)
        exp_score = 1.0 if cand_exp >= target_exp else (cand_exp / target_exp if target_exp > 0 else 1.0)

        # Protected career gaps must NEVER reduce readiness
        overall_readiness = int(
            round((skill_score * 0.60 + project_score * 0.25 + exp_score * 0.15) * 100)
        )

        return {
            "readiness_score": overall_readiness,
            "status": "Ready for Applications" if overall_readiness >= 80 else ("Developing" if overall_readiness >= 50 else "Early Preparation"),
            "skill_readiness": int(skill_score * 100),
            "project_readiness": int(project_score * 100),
            "experience_readiness": int(exp_score * 100),
        }
