from __future__ import annotations
from typing import Dict, List, Any


class RecommendationEngine:
    """Deterministic engine to match courses & certifications to skill gaps and generate ordered learning sequences."""

    def recommend_courses(
        self,
        skill_gaps: List[Dict[str, Any]],
        courses: List[Dict[str, Any]],
        candidate_level: str = "beginner",
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """Matches available courses to prioritized skill gaps."""
        if not skill_gaps:
            return []

        # Map gaps by skill name lowercased
        gap_skills = {
            g.get("skill", "").lower(): g for g in skill_gaps
        }

        matched_courses = []
        for course in courses:
            c_skills = [s.lower() for s in course.get("skills", [])]
            # Check overlap with gaps
            overlap = [s for s in c_skills if s in gap_skills]
            if overlap:
                target_gap = gap_skills[overlap[0]]
                priority = target_gap.get("priority", "medium")
                priority_boost = 1.5 if priority == "high" else (1.2 if priority == "medium" else 1.0)
                
                score = round(course.get("rating", 4.5) * priority_boost, 2)
                matched_courses.append({
                    "title": course.get("title", ""),
                    "platform": course.get("platform", "Online"),
                    "primary_skill": target_gap.get("skill", overlap[0].title()),
                    "priority": priority,
                    "duration_hours": course.get("duration_hours", 10),
                    "url": course.get("url", ""),
                    "score": score,
                })

        # Sort courses by priority (high > medium > low) and then by score descending
        prio_map = {"high": 0, "medium": 1, "low": 2}
        matched_courses.sort(key=lambda x: (prio_map[x["priority"]], -x["score"]))

        return matched_courses[:top_k]
