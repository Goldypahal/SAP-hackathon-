from __future__ import annotations
from typing import Any, Dict
from agents import (
    CareerResearchAgent,
    SkillAnalysisAgent,
    LearningAgent,
    OpportunityAgent,
    IndustryIntelligenceAgent,
    ProfileIntelligenceAgent,
)
from models.schemas import AgentResult


class AgentOrchestrator:
    """Agent Orchestrator: Coordinates multi-agent workflow, managing context & shared intelligence state."""

    def __init__(
        self,
        career_research: CareerResearchAgent = None,
        skill_analysis: SkillAnalysisAgent = None,
        learning: LearningAgent = None,
        opportunity: OpportunityAgent = None,
        industry_intelligence: IndustryIntelligenceAgent = None,
        profile_intelligence: ProfileIntelligenceAgent = None,
    ):
        self.career_research = career_research or CareerResearchAgent()
        self.skill_analysis = skill_analysis or SkillAnalysisAgent()
        self.learning = learning or LearningAgent()
        self.opportunity = opportunity or OpportunityAgent()
        self.industry_intelligence = industry_intelligence or IndustryIntelligenceAgent()
        self.profile_intelligence = profile_intelligence or ProfileIntelligenceAgent()

    def run_career_pipeline(self, initial_context: Dict[str, Any]) -> Dict[str, Any]:
        """Executes full six-agent pipeline and returns consolidated Career Intelligence State."""
        context = dict(initial_context)
        agent_results: Dict[str, AgentResult] = {}

        # 1. Skill Analysis Agent
        skill_res = self.skill_analysis.execute(context)
        agent_results["skill_analysis"] = skill_res
        if skill_res.status == "success":
            context["skill_gaps"] = skill_res.data.get("skill_gaps", [])
            context["strengths"] = skill_res.data.get("strengths", [])

        # 2. Career Research Agent
        career_res = self.career_research.execute(context)
        agent_results["career_research"] = career_res

        # 3. Industry Intelligence Agent
        industry_res = self.industry_intelligence.execute(context)
        agent_results["industry_intelligence"] = industry_res

        # 4. Learning Agent
        learning_res = self.learning.execute(context)
        agent_results["learning"] = learning_res
        if learning_res.status == "success":
            context["recommended_courses"] = learning_res.data.get("recommended_courses", [])
            context["learning_plan"] = learning_res.data.get("learning_plan", [])

        # 5. Opportunity Agent
        opportunity_res = self.opportunity.execute(context)
        agent_results["opportunity"] = opportunity_res

        # 6. Profile Intelligence Agent
        profile_res = self.profile_intelligence.execute(context)
        agent_results["profile_intelligence"] = profile_res

        # Assemble final state
        state = {
            "candidate_id": context.get("candidate", {}).get("candidate_id", "unknown"),
            "target_role": context.get("target_role", {}).get("name", "Target Role"),
            "agent_summaries": {name: res.summary for name, res in agent_results.items()},
            "agent_explanations": {name: res.data.get("explanation", "") for name, res in agent_results.items() if res.data and "explanation" in res.data},
            "strengths": context.get("strengths", []),
            "skill_gaps": context.get("skill_gaps", []),
            "career_paths": career_res.data.get("career_paths", []),
            "skill_trends": industry_res.data.get("skill_trends", []),
            "emerging_skills": industry_res.data.get("emerging_skills", []),
            "learning_plan": learning_res.data.get("learning_plan", []),
            "certifications": learning_res.data.get("certifications", []),
            "matched_opportunities": opportunity_res.data.get("matched_opportunities", []),
            "readiness": profile_res.data.get("readiness", {}),
            "roadmap": profile_res.data.get("roadmap", []),
        }

        return state
