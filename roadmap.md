1. Overall Agent Architecture

I recommend this:

                         USER PROFILE
                              │
                    ┌─────────▼─────────┐
                    │  AGENT ORCHESTRATOR │
                    └─────────┬─────────┘
                              │
       ┌──────────┬───────────┼───────────┬───────────┐
       ▼          ▼           ▼           ▼           ▼
   CAREER      SKILL       LEARNING   OPPORTUNITY  INDUSTRY
   RESEARCH   ANALYSIS       AGENT       AGENT    INTELLIGENCE
     AGENT       AGENT                                   AGENT
       │          │           │           │              │
       └──────────┴───────────┼───────────┴──────────────┘
                              ▼
                    PROFILE INTELLIGENCE
                           AGENT
                              │
                              ▼
                       SHARED STATE
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                  RAG               LLM/AI
               Knowledge            Reasoning

The important design decision:

Agents should orchestrate intelligence. They should not independently calculate everything.

For example, Skill Analysis Agent can call a SkillGapEngine, while Opportunity Agent can call a MatchingEngine.

2. Shared Data Model

Before writing the six agents, create a common data structure.

Every agent should understand something like:

CandidateProfile
    ├── candidate_id
    ├── education
    ├── experience
    ├── skills
    ├── projects
    ├── certifications
    ├── courses
    ├── target_roles
    └── preferences

Skill:

Skill
    ├── name
    ├── normalized_name
    ├── proficiency
    ├── evidence
    ├── experience_months
    └── last_used

Target role:

TargetRole
    ├── role_name
    ├── required_skills
    ├── preferred_skills
    ├── experience_requirement
    └── education_requirement

This becomes the common language between agents.

3. Career Research Agent
SRS responsibilities

Your SRS says this agent should:

Research career paths
Identify emerging opportunities
Analyze career trends
Suggest career alternatives
Architecture
Candidate Profile
       │
       ▼
Career Research Agent
       │
       ├── O*NET
       ├── ESCO
       ├── Job Market Data
       ├── RAG
       └── Market Intelligence
              │
              ▼
        Career Analysis
Input
{
  "candidate_profile": {},
  "current_role": "Data Analyst",
  "target_role": "Data Scientist"
}
Processing

It should determine:

Current career
       ↓
Possible career paths
       ↓
Target career
       ↓
Alternative careers
       ↓
Market demand
       ↓
Emerging opportunities
Output
{
  "agent": "career_research",
  "career_paths": [
    {
      "role": "Data Scientist",
      "fit_score": 0.87
    },
    {
      "role": "ML Engineer",
      "fit_score": 0.76
    }
  ],
  "emerging_opportunities": [],
  "career_trends": [],
  "alternatives": []
}
Important

This agent should not invent career trends.

Your SRS says real market information should come from processed job data rather than being invented by the LLM.

4. Skill Analysis Agent ⭐

This is probably your most important agent.

SRS responsibilities
Analyze candidate skills
Compare skills with target roles
Identify missing skills
Prioritize skill gaps
Architecture
Candidate Profile
       │
       ▼
Skill Analysis Agent
       │
       ├── Skill Normalizer
       ├── O*NET / ESCO
       ├── Role Requirements
       └── Skill Gap Engine
                │
                ▼
           Skill Analysis
Example

Candidate:

Python       85%
SQL          75%
Pandas       80%
Docker       20%
Kubernetes    0%
MLOps         0%

Target:

ML Engineer

Agent produces:

Strong:
Python
Pandas

Moderate:
SQL

Gap:
Docker
Kubernetes
MLOps

Then prioritize:

1. Docker       HIGH
2. MLOps        HIGH
3. Kubernetes   MEDIUM
Output
{
  "agent": "skill_analysis",
  "target_role": "ML Engineer",
  "strengths": [],
  "skill_gaps": [
    {
      "skill": "Docker",
      "priority": "high",
      "current_level": 0.2,
      "required_level": 0.7
    }
  ]
}

This agent should call your deterministic Skill Gap Engine, rather than asking an LLM to calculate the gap.

5. Learning Agent
SRS responsibilities
Find relevant courses
Recommend certifications
Match learning resources to gaps
Generate learning sequences
Architecture
Skill Gaps
     │
     ▼
Learning Agent
     │
     ├── Course Database
     ├── Skill ↔ Course Mapping
     ├── Certification Database
     └── Recommendation Engine
             │
             ▼
       Learning Plan
Example

Input:

Skill Gap:
Docker
MLOps
Kubernetes

Output:

Step 1
Docker fundamentals

Step 2
Containerize ML application

Step 3
Kubernetes fundamentals

Step 4
MLOps pipeline

Step 5
Deploy ML model

The key is sequence, not simply a list of courses.

Output
{
  "agent": "learning",
  "learning_plan": [
    {
      "skill": "Docker",
      "resources": [],
      "priority": 1
    },
    {
      "skill": "MLOps",
      "resources": [],
      "priority": 2
    }
  ],
  "certifications": []
}
6. Opportunity Agent ⭐
SRS responsibilities
Match internships
Match entry-level jobs
Identify suitable opportunities
Calculate compatibility
Architecture
Candidate Profile
       │
       ▼
Opportunity Agent
       │
       ├── Job Database
       ├── Skill Matcher
       ├── Experience Matcher
       ├── Education Matcher
       └── Preference Matcher
               │
               ▼
        Compatibility Score

Example:

Job A

Skill Match       92%
Experience Match  85%
Education Match   100%
Location Match    100%

Overall           91%

And explain:

WHY MATCHED

✓ Python
✓ SQL
✓ Machine Learning
✓ Pandas

GAPS

⚠ AWS
⚠ Docker

This explanation capability aligns with your SRS's explainability requirement.

7. Industry Intelligence Agent ⭐⭐⭐

This is another potentially very strong differentiator.

SRS responsibilities
Monitor technology trends
Analyze changing skill requirements
Identify emerging tools
Architecture
                    Job Market Data
                           │
        ┌──────────────────┼─────────────────┐
        ▼                  ▼                 ▼
   Current Jobs       Historical Jobs    Tech Data
        │                  │                 │
        └──────────────────┼─────────────────┘
                           ▼
              Industry Intelligence Agent
                           │
                    Trend Analyzer
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          Skill Trends  Tool Trends  Demand Trends

For example:

Skill          Current Demand    Trend
Python              72%            →
SQL                 64%            →
Docker              41%            ↑
Kubernetes          29%            ↑
MLOps               24%            ↑↑

The agent can then tell the user:

"MLOps demand is increasing among ML engineering roles, so it has been elevated in your roadmap."

That's much more defensible than:

"AI says MLOps is important."

8. Profile Intelligence Agent
SRS responsibilities
Analyze user progress
Track projects
Evaluate resume improvements
Monitor career readiness
Architecture
User Activity
     │
     ├── Courses
     ├── Projects
     ├── Certifications
     ├── Skills
     ├── Resume
     └── Applications
            │
            ▼
 Profile Intelligence Agent
            │
       Progress Analyzer
            │
      ┌─────┼─────┐
      ▼     ▼     ▼
   Skills Projects Readiness

Example:

Previous Profile

Python       70%
Docker       10%
ML           60%

        ↓

Completed:
✓ Docker course
✓ ML deployment project

        ↓

Updated Profile

Python       70%
Docker       55%
ML           72%

This agent is what makes the platform continuous, rather than a one-time recommendation system.

9. The Orchestrator

I strongly recommend creating one more component:

AgentOrchestrator

This doesn't replace your six agents.

It coordinates them.

                    Orchestrator
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
Career Research    Skill Analysis     Industry Intel
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ↓
                    Learning Agent
                         │
                         ↓
                  Opportunity Agent
                         │
                         ↓
                Profile Intelligence

For example, when a new resume is uploaded:

Resume
  ↓
Profile Intelligence
  ↓
Skill Analysis
  ↓
Career Research
  ↓
Industry Intelligence
  ↓
Learning
  ↓
Opportunity
  ↓
Updated Profile
10. Shared State

This is extremely important.

Don't let each agent maintain its own copy of the user.

Create:

Career Intelligence State

Example:

{
  "candidate": {},
  "skills": [],
  "target_roles": [],
  "skill_gaps": [],
  "learning_progress": [],
  "projects": [],
  "market_intelligence": {},
  "opportunities": [],
  "readiness": {},
  "roadmap": []
}

Agents read and update specific portions of this state.

11. What should use LLM vs normal code?

This is where I would be strict.

Component	LLM?	Normal algorithm?
Resume extraction	✅	✅
Skill normalization	Maybe	✅
Skill gap calculation	❌	✅
Skill prioritization	Maybe	✅
Job matching	❌/Maybe	✅
Course ranking	❌/Maybe	✅
Market statistics	❌	✅
Trend calculation	❌	✅
Career explanation	✅	
Roadmap explanation	✅	
Career Q&A	✅	
Resume feedback	✅	
Recommendation reasoning	✅	
RAG		✅
Agent coordination	Maybe	✅

Don't make the LLM responsible for numerical truth.

12. Suggested project structure

I'd create your AI layer like this:

ai-career-engine/
│
├── agents/
│   ├── career_research_agent.py
│   ├── skill_analysis_agent.py
│   ├── learning_agent.py
│   ├── opportunity_agent.py
│   ├── industry_intelligence_agent.py
│   └── profile_intelligence_agent.py
│
├── engines/
│   ├── resume_engine.py
│   ├── skill_engine.py
│   ├── skill_gap_engine.py
│   ├── matching_engine.py
│   ├── recommendation_engine.py
│   ├── market_engine.py
│   ├── readiness_engine.py
│   └── roadmap_engine.py
│
├── rag/
│   ├── retriever.py
│   ├── embeddings.py
│   ├── reranker.py
│   └── knowledge_base.py
│
├── orchestrator/
│   └── agent_orchestrator.py
│
├── models/
│   ├── candidate.py
│   ├── skill.py
│   ├── opportunity.py
│   └── responses.py
│
├── config/
│   └── settings.py
│
├── tests/
│   ├── test_skill_agent.py
│   ├── test_learning_agent.py
│   ├── test_opportunity_agent.py
│   └── test_orchestrator.py
│
├── examples/
│   └── sample_candidate.json
│
├── requirements.txt
└── README.md
13. Build order

I recommend not starting with Career Research Agent.

Build in this order:

STEP 1
Shared data models
        ↓
STEP 2
Skill Intelligence
        ↓
STEP 3
Skill Gap Engine
        ↓
STEP 4
Skill Analysis Agent
        ↓
STEP 5
Learning Agent
        ↓
STEP 6
Opportunity Agent
        ↓
STEP 7
Career Research Agent
        ↓
STEP 8
Industry Intelligence Agent
        ↓
STEP 9
Profile Intelligence Agent
        ↓
STEP 10
Orchestrator
        ↓
STEP 11
RAG integration
        ↓
STEP 12
Tests + API contract
        ↓
GITHUB
The first milestone I'd target

Get this working without any frontend or backend:

candidate.json
      ↓
Skill Analysis Agent
      ↓
Skill Gap Engine
      ↓
Learning Agent
      ↓
Opportunity Agent
      ↓
structured JSON

If you can run:

python demo.py

and get:

Candidate
   ↓
Skills detected
   ↓
Target role
   ↓
Skill gaps
   ↓
Prioritized gaps
   ↓
Courses
   ↓
Job matches