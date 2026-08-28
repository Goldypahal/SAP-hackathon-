from __future__ import annotations
from typing import Dict, List, Any


class MatchingEngine:
    """Deterministic engine to match candidate profile against job opportunities.
    Includes sub-scores (Skill, Experience, Education, Location), overall compatibility score,
    and transparent explainability (WHY MATCHED vs GAPS).
    Career gaps marked as protected NEVER reduce matching or readiness scores.
    """

    def rank(
        self,
        candidate: Dict[str, Any],
        opportunities: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Ranks list of opportunity dicts against candidate profile."""
        cand_skills = set(
            s.lower() for s in candidate.get("skills", [])
        )
        cand_exp = candidate.get("experience_years", 0.0)
        cand_edu = [e.lower() for e in candidate.get("education", [])]
        cand_loc = candidate.get("location", "").lower()

        # Ignore protected career gaps in experience calculation (do not deduct)
        # Career gaps are passed for audit but explicitly protected

        ranked = []
        for opp in opportunities:
            opp_title = opp.get("title", "Unknown Role")
            opp_company = opp.get("company", "Company")
            req_skills = opp.get("required_skills", [])
            pref_skills = opp.get("preferred_skills", [])
            req_exp = opp.get("experience_required", 0.0)
            req_edu = opp.get("education_required", "")
            opp_loc = opp.get("location", "").lower()

            # 1. Skill Match Calculation
            matched_skills = []
            missing_skills = []

            all_target_skills = req_skills + pref_skills
            if not all_target_skills:
                skill_score = 1.0
            else:
                matched_count = 0
                for s in req_skills:
                    if s.lower() in cand_skills:
                        matched_count += 1
                        matched_skills.append(s)
                    else:
                        missing_skills.append(s)
                
                for s in pref_skills:
                    if s.lower() in cand_skills:
                        matched_count += 0.5
                        matched_skills.append(s)
                    else:
                        if s not in missing_skills:
                            missing_skills.append(s)
                
                max_score = len(req_skills) + (0.5 * len(pref_skills))
                skill_score = min(1.0, matched_count / max_score) if max_score > 0 else 1.0

            # 2. Experience Match Calculation
            if req_exp <= 0 or cand_exp >= req_exp:
                exp_score = 1.0
            else:
                exp_score = round(cand_exp / req_exp, 2)

            # 3. Education Match Calculation
            if not req_edu:
                edu_score = 1.0
            else:
                edu_score = 1.0 if any(req_edu.lower() in e for e in cand_edu) else 0.80

            # 4. Location Match Calculation
            if not opp_loc or opp_loc == "remote" or cand_loc == opp_loc:
                loc_score = 1.0
            else:
                loc_score = 0.75

            # Overall Score (Weighted: Skill 50%, Experience 25%, Education 15%, Location 10%)
            overall_score = round(
                (skill_score * 0.50) +
                (exp_score * 0.25) +
                (edu_score * 0.15) +
                (loc_score * 0.10),
                2,
            )

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
