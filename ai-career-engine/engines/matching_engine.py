from __future__ import annotations
from typing import Dict, List, Any
from engines.skill_engine import SkillEngine


def calculate_effective_experience(experience_years: float, career_gaps: List[Dict[str, Any]]) -> float:
    """Calculates effective experience by restoring time spent on protected career gaps.
    Strictly checks that g.get("protected") is True to prevent accidental score inflation.
    """
    protected_months = sum(
        g.get("duration_months", 0) for g in (career_gaps or []) if g.get("protected") is True
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
        """Ranks list of opportunity dicts against candidate profile using continuous proficiency-weighted matching."""
        cand_skill_map: Dict[str, float] = {}
        raw_skills = candidate.get("skills", [])
        for s in raw_skills:
            if isinstance(s, dict):
                norm = s.get("normalized_name") or self.skill_engine.normalize_skill_name(s.get("name", ""))
                norm = self.skill_engine.normalize_skill_name(norm)
                prof = min(1.0, max(0.0, float(s.get("proficiency", 0.0))))
                cand_skill_map[norm] = prof
            elif isinstance(s, str):
                norm = self.skill_engine.normalize_skill_name(s)
                cand_skill_map[norm] = 1.0

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

            # 1. Continuous Proficiency-Weighted Skill Match Calculation
            if not req_skills:
                skill_score = 1.0
                matched_skills = []
                missing_skills = []
            else:
                req_scores = []
                matched_skills = []
                missing_skills = []

                for r_skill in req_skills:
                    if isinstance(r_skill, dict):
                        r_name = r_skill.get("name", "")
                        r_norm = r_skill.get("normalized_name") or self.skill_engine.normalize_skill_name(r_name)
                        r_req_level = min(1.0, max(0.0, float(r_skill.get("proficiency", 0.60))))
                    else:
                        r_name = str(r_skill)
                        r_norm = self.skill_engine.normalize_skill_name(r_name)
                        r_req_level = 0.60


                    r_norm = self.skill_engine.normalize_skill_name(r_norm)
                    c_prof = cand_skill_map.get(r_norm, 0.0)

                    ratio = min(1.0, c_prof / r_req_level) if r_req_level > 0 else 1.0
                    req_scores.append(ratio)

                    display_name = r_name if r_name else r_norm.title()
                    if c_prof >= skill_proficiency_threshold:
                        matched_skills.append(display_name)
                    if c_prof < r_req_level:
                        missing_skills.append(display_name)

                req_avg_score = sum(req_scores) / len(req_scores) if req_scores else 1.0

                if pref_skills:
                    pref_scores = []
                    for p_skill in pref_skills:
                        if isinstance(p_skill, dict):
                            p_name = p_skill.get("name", "")
                            p_norm = p_skill.get("normalized_name") or self.skill_engine.normalize_skill_name(p_name)
                            p_req_level = min(1.0, max(0.0, float(p_skill.get("proficiency", 0.50))))
                        else:
                            p_name = str(p_skill)
                            p_norm = self.skill_engine.normalize_skill_name(p_name)
                            p_req_level = 0.50

                        p_norm = self.skill_engine.normalize_skill_name(p_norm)
                        c_prof = cand_skill_map.get(p_norm, 0.0)
                        ratio = min(1.0, c_prof / p_req_level) if p_req_level > 0 else 1.0
                        pref_scores.append(ratio)

                        display_name = p_name if p_name else p_norm.title()
                        if c_prof >= skill_proficiency_threshold and display_name not in matched_skills:
                            matched_skills.append(display_name)

                    pref_avg_score = sum(pref_scores) / len(pref_scores) if pref_scores else 1.0
                    skill_score = (req_avg_score * 0.85) + (pref_avg_score * 0.15)
                else:
                    skill_score = req_avg_score

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
                elif any("bachelor" in e or "master" in e or "phd" in e or "degree" in e for e in cand_edu):
                    edu_score = 0.75
                else:
                    edu_score = 0.45

            # 4. Location Match Calculation
            work_mode = opp.get("work_mode", "").lower()
            if not opp_loc or "remote" in opp_loc or "remote" in work_mode or any(c_loc in opp_loc for c_loc in cand_loc.split(",") if c_loc):
                loc_score = 1.0
            elif "hybrid" in opp_loc or "hybrid" in work_mode:
                loc_score = 0.75
            else:
                loc_score = 0.40

            # Overall Score (Weighted: Skill 50%, Experience 25%, Education 15%, Location 10%)
            overall_score = round(
                (skill_score * 0.50) +
                (exp_score * 0.25) +
                (edu_score * 0.15) +
                (loc_score * 0.10),
                2,
            )

            # Target role title alignment boost (+0.10) if opportunity matches target role
            if target_role_name and (target_role_name.lower() in opp_title.lower() or opp_title.lower() in target_role_name.lower()):
                overall_score = min(1.0, overall_score + 0.10)


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

        # Sort by compatibility score descending, breaking ties with total matched skills count
        ranked.sort(key=lambda x: (x["compatibility_score"], len(x["why_matched"])), reverse=True)
        return ranked


