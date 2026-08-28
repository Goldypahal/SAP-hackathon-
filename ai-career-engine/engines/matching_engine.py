from __future__ import annotations
from typing import Dict, List, Any
from engines.skill_engine import SkillEngine


def calculate_effective_experience(experience_years: float, career_gaps: List[Dict[str, Any]]) -> float:
    """Calculates effective experience by restoring time spent on protected career gaps."""
    protected_months = sum(
        g.get("duration_months", 0) for g in (career_gaps or []) if g.get("protected", True)
    )
    return round(experience_years + (protected_months / 12.0), 2)


class MatchingEngine:
    """Deterministic engine to match candidate profile against job opportunities.
    Includes sub-scores (Skill, Experience, Education, Location), overall compatibility score,
    and transparent explainability (WHY MATCHED vs GAPS).
    Career gaps marked as protected NEVER reduce matching or readiness scores.
    """

    def __init__(self, skill_engine: SkillEngine = None):
        self.skill_engine = skill_engine or SkillEngine()

    def rank(
        self,
        candidate: Dict[str, Any],
        opportunities: List[Dict[str, Any]],
        skill_proficiency_threshold: float = 0.30,
        target_role_name: str = "",
    ) -> List[Dict[str, Any]]:
        """Ranks list of opportunity dicts against candidate profile."""
        cand_skills = set()
        raw_skills = candidate.get("skills", [])
        for s in raw_skills:
            if isinstance(s, dict):
                if float(s.get("proficiency", 0.0)) >= skill_proficiency_threshold:
                    norm = s.get("normalized_name") or self.skill_engine.normalize_skill_name(s.get("name", ""))
                    cand_skills.add(self.skill_engine.normalize_skill_name(norm))
            elif isinstance(s, str):
                cand_skills.add(self.skill_engine.normalize_skill_name(s))

        cand_exp = calculate_effective_experience(
            candidate.get("experience_years", 0.0),
            candidate.get("career_gaps", []),
        )
        cand_edu = [e.lower() for e in candidate.get("education", [])]
        cand_loc = candidate.get("location", "").lower()

        ranked = []
        for opp in opportunities:
            opp_title = opp.get("title", "Unknown Role")
            opp_company = opp.get("company", "Company")
            req_skills = opp.get("required_skills", [])
            pref_skills = opp.get("preferred_skills", [])
            req_exp = opp.get("experience_min", opp.get("experience_required", 0.0))
            req_edu = opp.get("education_required", opp.get("education", []))
            opp_loc = opp.get("location", "").lower()

            # 1. Skill Match Calculation
            if not req_skills:
                skill_score = 1.0
                matched_skills = []
                missing_skills = []
            else:
                req_matched = [s for s in req_skills if self.skill_engine.normalize_skill_name(s) in cand_skills]
                req_missing = [s for s in req_skills if self.skill_engine.normalize_skill_name(s) not in cand_skills]
                req_score = len(req_matched) / len(req_skills)

                if req_score == 1.0:
                    skill_score = 1.0
                    matched_skills = req_matched + ([s for s in pref_skills if self.skill_engine.normalize_skill_name(s) in cand_skills])
                elif pref_skills:
                    pref_matched = [s for s in pref_skills if self.skill_engine.normalize_skill_name(s) in cand_skills]
                    pref_score = len(pref_matched) / len(pref_skills)
                    skill_score = (req_score * 0.85) + (pref_score * 0.15)
                    matched_skills = req_matched + pref_matched
                else:
                    skill_score = req_score
                    matched_skills = req_matched


                missing_skills = req_missing

            # 2. Experience Match Calculation (Using Effective Experience)
            if req_exp <= 0 or cand_exp >= req_exp:
                exp_score = 1.0
            else:
                exp_score = round(cand_exp / req_exp, 2)

            # 3. Education Match Calculation
            if not req_edu:
                edu_score = 1.0
            else:
                edu_list = req_edu if isinstance(req_edu, list) else [req_edu]
                if any(any(req_item.lower() in e for e in cand_edu) for req_item in edu_list):
                    edu_score = 1.0
                else:
                    edu_score = 0.80

            # 4. Location Match Calculation
            if not opp_loc or "remote" in opp_loc or "hybrid" in opp.get("work_mode", "").lower() or any(c_loc in opp_loc for c_loc in cand_loc.split(",")):
                loc_score = 1.0
            else:
                loc_score = 0.85

            # Overall Score (Weighted: Skill 50%, Experience 25%, Education 15%, Location 10%)
            overall_score = round(
                (skill_score * 0.50) +
                (exp_score * 0.25) +
                (edu_score * 0.15) +
                (loc_score * 0.10),
                2,
            )

            # Target role title alignment boost (+0.05) if opportunity matches target role
            if target_role_name and target_role_name.lower() in opp_title.lower():
                overall_score = min(1.0, overall_score + 0.05)

            ranked.append({
                "title": opp_title,
                "company": opp_company,
                "compatibility_score": int(overall_score * 100),
                "breakdown": {
                    "skill_match": int(skill_score * 100),
                    "experience_match": int(exp_score * 100),
                    "education_match": int(edu_score * 100),
                    "location_match": int(loc_score * 100),
                },
                "why_matched": matched_skills,
                "gaps": missing_skills,
            })

        # Sort by compatibility score descending
        ranked.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return ranked
