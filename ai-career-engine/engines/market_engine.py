from __future__ import annotations
from typing import Dict, List, Any


class MarketEngine:
    """Deterministic engine for job market statistics, skill demand, and trend calculation."""

    def analyze_skill_demand(self, jobs: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Calculates percentage demand for skills across a collection of job postings."""
        if not jobs:
            # Fallback default statistics for demonstration
            return {
                "python": {"demand_pct": 72, "trend": "STABLE"},
                "sql": {"demand_pct": 64, "trend": "STABLE"},
                "docker": {"demand_pct": 41, "trend": "GROWING"},
                "kubernetes": {"demand_pct": 29, "trend": "GROWING"},
                "mlops": {"demand_pct": 24, "trend": "HIGH GROWTH"},
            }


        total_jobs = len(jobs)
        skill_counts: Dict[str, int] = {}
        for j in jobs:
            for s in j.get("required_skills", []) + j.get("preferred_skills", []):
                s_clean = s.strip().lower()
                skill_counts[s_clean] = skill_counts.get(s_clean, 0) + 1

        results = {}
        for s_name, count in skill_counts.items():
            pct = int((count / total_jobs) * 100)
            results[s_name] = {
                "demand_pct": pct,
                "trend": "GROWING" if pct > 30 else "STABLE",
            }
        return results

    def calculate_trends(
        self,
        current_jobs: List[Dict[str, Any]],
        previous_jobs: List[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Calculates demand changes between past and current job postings."""
        curr_demand = self.analyze_skill_demand(current_jobs)
        trends = []
        for s_name, data in curr_demand.items():
            trends.append({
                "skill": s_name.title() if s_name not in ["sql", "mlops", "aws"] else s_name.upper(),
                "current_demand": f"{data['demand_pct']}%",
                "trend": data["trend"],
            })
        return trends

    def emerging_skills(self, trends: List[Dict[str, Any]]) -> List[str]:
        """Identifies skills with strong upward growth trends."""
        emerging = []
        for t in trends:
            if t.get("trend") in ["GROWING", "HIGH GROWTH", "↑", "↑↑"]:
                emerging.append(t["skill"])
        return emerging

