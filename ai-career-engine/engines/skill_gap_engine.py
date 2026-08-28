from __future__ import annotations
from typing import Dict, List, Any
from models.schemas import Skill, SkillGap, Priority


class SkillGapEngine:
    """Deterministic calculation of skill gaps between candidate and target role requirements."""

    def analyze(
        self,
        candidate_skills: List[Dict[str, Any]],
        required_skills: List[Dict[str, Any]],
        preferred_skills: List[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Calculates exact numerical gap for each required/preferred skill and prioritizes them."""
        preferred_skills = preferred_skills or []
        
        # Build map of candidate skills by normalized name
        cand_map: Dict[str, float] = {}
        for s in candidate_skills:
            name = s.get("normalized_name") or s.get("name", "").strip().lower()
            prof = float(s.get("proficiency", 0.0))
            cand_map[name] = prof

        gaps: List[SkillGap] = []

        # Analyze required skills
        for r_skill in required_skills:
            r_name = r_skill.get("normalized_name") or r_skill.get("name", "").strip().lower()
            req_level = float(r_skill.get("proficiency", 0.7))
            curr_level = cand_map.get(r_name, 0.0)
            
            if curr_level < req_level:
                gap_val = round(req_level - curr_level, 2)
                # Determine priority based on gap magnitude
                if gap_val >= 0.5 or curr_level == 0.0:
                    priority: Priority = "high"
                elif gap_val >= 0.25:
                    priority: Priority = "medium"
                else:
                    priority: Priority = "low"

                gaps.append(
                    SkillGap(
                        skill=r_skill.get("name", r_name.title()),
                        required_level=req_level,
                        current_level=curr_level,
                        gap=gap_val,
                        priority=priority,
                        evidence=[f"Required by target role (minimum level: {req_level})"],
                    )
                )

        # Analyze preferred skills
        for p_skill in preferred_skills:
            p_name = p_skill.get("normalized_name") or p_skill.get("name", "").strip().lower()
            req_level = float(p_skill.get("proficiency", 0.5))
            curr_level = cand_map.get(p_name, 0.0)

            if curr_level < req_level and not any(g.skill.lower() == p_name for g in gaps):
                gap_val = round(req_level - curr_level, 2)
                gaps.append(
                    SkillGap(
                        skill=p_skill.get("name", p_name.title()),
                        required_level=req_level,
                        current_level=curr_level,
                        gap=gap_val,
                        priority="low",
                        evidence=[f"Preferred skill for role (target level: {req_level})"],
                    )
                )

        # Sort gaps by priority (high first, medium second, low third) and then by gap size descending
        priority_order = {"high": 0, "medium": 1, "low": 2}
        gaps.sort(key=lambda x: (priority_order[x.priority], -x.gap))

        return [g.model_dump() for g in gaps]
