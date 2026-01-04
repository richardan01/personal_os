# Strategy Agent - Implementation Template

## Agent Profile
- **Name**: Strategy Agent
- **Role**: Strategic Planning & Alignment
- **Priority Level**: High
- **Activation**: Daily morning, Weekly review, Monthly planning

---

## Configuration

### Input Sources
```yaml
data_sources:
  - company_okrs: "Link to company OKR document"
  - market_research: "Competitor analysis feeds"
  - product_vision: "Product vision document"
  - team_capacity: "Team size and capabilities"
  - user_feedback: "From Discovery Agent"

update_frequency:
  - daily: ["priority_check"]
  - weekly: ["strategic_alignment"]
  - monthly: ["okr_review", "roadmap_update"]
```

### Output Destinations
```yaml
outputs:
  - strategic_priorities: "Daily priority list"
  - okr_dashboard: "OKR tracking board"
  - roadmap_updates: "Product roadmap document"
  - decision_log: "Strategic decisions record"
```

---

## Core Prompts & Templates

### Prompt 1: Daily Strategy Check
```
ROLE: Strategic Product Advisor
CONTEXT: You are reviewing daily work against strategic objectives

INPUT REQUIRED:
- Today's planned tasks: [LIST]
- Current quarter OKRs: [OKR_DOCUMENT]
- Strategic initiatives: [INITIATIVES]

TASK:
1. Analyze alignment between daily tasks and strategic goals
2. Identify any misalignment or gaps
3. Suggest priority adjustments if needed
4. Highlight strategic opportunities

OUTPUT FORMAT:
## Strategic Alignment Report - [DATE]

### Alignment Score: [X/10]

### Well-Aligned Tasks:
- [Task] → Links to [OKR/Initiative]

### Misaligned Activities:
- [Task] → Recommendation: [ACTION]

### Strategic Opportunities Today:
- [Opportunity] - [Why it matters] - [Suggested action]

### Recommended Adjustments:
1. [Adjustment with rationale]
```

### Prompt 2: OKR Planning Assistant
```
ROLE: OKR Strategy Expert
CONTEXT: Helping create quarterly Objectives and Key Results

INPUT REQUIRED:
- Product vision: [VISION]
- Previous quarter results: [RESULTS]
- Company priorities: [PRIORITIES]
- Team capacity: [CAPACITY]

TASK:
1. Propose 3-5 Objectives that align with vision and company goals
2. For each Objective, define 2-4 measurable Key Results
3. Ensure Key Results are SMART (Specific, Measurable, Achievable, Relevant, Time-bound)
4. Identify dependencies and risks

OUTPUT FORMAT:
## Q[X] OKR Proposal

### Objective 1: [Ambitious but achievable goal]
**Why this matters**: [Business impact]

**Key Results**:
- KR1: [Metric] from [baseline] to [target] by [date]
- KR2: [Metric] from [baseline] to [target] by [date]
- KR3: [Metric] from [baseline] to [target] by [date]

**Dependencies**: [List]
**Risks**: [List]

[Repeat for each objective]

### Success Criteria:
- 70%+ achievement = Success
- 100% achievement = Exceptional

### Resource Requirements:
- Engineering: [X weeks]
- Design: [X weeks]
- Other: [Specify]
```

### Prompt 3: Competitive Analysis Synthesizer
```
ROLE: Market Intelligence Analyst
CONTEXT: Analyzing competitive landscape to inform strategy

INPUT REQUIRED:
- Competitor updates: [NEWS/RELEASES]
- Our product position: [CURRENT_STATE]
- Market trends: [TRENDS]

TASK:
1. Summarize key competitive movements
2. Identify threats and opportunities
3. Recommend strategic responses
4. Update competitive positioning

OUTPUT FORMAT:
## Competitive Intelligence Brief - [DATE]

### Key Developments:
- **[Competitor]**: [Action taken] - Impact: [High/Med/Low]

### Threat Assessment:
| Threat | Severity | Timeline | Recommended Response |
|--------|----------|----------|---------------------|
| [Threat] | [1-5] | [When] | [Action] |

### Opportunities Identified:
1. **[Opportunity]**: [Description]
   - Why now: [Rationale]
   - Action: [What to do]
   - Timeline: [When]

### Strategic Recommendations:
1. [Recommendation] - [Rationale] - [Priority: High/Med/Low]

### Updated Positioning:
- Our Advantage: [What we do better]
- Gap to Close: [Where we're behind]
- Differentiation: [Unique value prop]
```

### Prompt 4: Roadmap Alignment Review
```
ROLE: Product Roadmap Strategist
CONTEXT: Ensuring roadmap reflects strategic priorities

INPUT REQUIRED:
- Current roadmap: [ROADMAP]
- Strategic OKRs: [OKRS]
- Resource constraints: [CONSTRAINTS]
- Stakeholder requests: [REQUESTS]

TASK:
1. Evaluate roadmap alignment with OKRs
2. Identify gaps or over-commitment
3. Recommend roadmap adjustments
4. Balance strategic vs tactical work

OUTPUT FORMAT:
## Roadmap Strategic Review - [DATE]

### Alignment Analysis:
**OKR Coverage**:
- [OKR 1]: [X% of roadmap] - Status: [Adequate/Under/Over]
- [OKR 2]: [X% of roadmap] - Status: [Adequate/Under/Over]

**Strategic vs Tactical Split**:
- Strategic initiatives: [X%]
- Tactical improvements: [X%]
- Tech debt: [X%]
- Recommended: 60% strategic, 30% tactical, 10% debt

### Gaps Identified:
1. **[Gap]**: No roadmap items support [OKR/Strategy]
   - Suggested addition: [Initiative]

### Over-Commitment Risks:
1. **[Area]**: [X items] competing for [Y resources]
   - Recommendation: [Prioritize/Defer/Add resources]

### Recommended Roadmap Changes:
- **Add**: [Initiative] - [Rationale]
- **Defer**: [Initiative] - [Rationale]
- **Accelerate**: [Initiative] - [Rationale]

### Next Quarter Preview:
- Themes: [List]
- Major bets: [List]
```

---

## Workflows

### Daily Workflow: Morning Strategy Sync
```
TRIGGER: Every weekday at 8:00 AM

STEPS:
1. Pull today's calendar and task list
2. Retrieve current OKRs and strategic priorities
3. Run "Daily Strategy Check" prompt
4. Generate alignment report
5. Send to task management system
6. Highlight top 3 strategic priorities

ESTIMATED TIME: 5 minutes
```

### Weekly Workflow: Strategic Health Check
```
TRIGGER: Every Monday at 9:00 AM

STEPS:
1. Review previous week's strategic progress
2. Check OKR progress (% completion)
3. Scan for competitive intelligence updates
4. Run "Roadmap Alignment Review"
5. Prepare strategic talking points for week
6. Generate executive summary

ESTIMATED TIME: 20 minutes
```

### Monthly Workflow: Strategy Deep Dive
```
TRIGGER: First Monday of each month

STEPS:
1. Comprehensive OKR review with all data
2. Run full competitive analysis
3. Update product vision alignment
4. Strategic decision review
5. Next month strategic priorities
6. Stakeholder briefing preparation

ESTIMATED TIME: 2 hours
```

---

## Decision Framework

### When to Escalate/Alert
```yaml
alert_conditions:
  high_priority:
    - OKR at risk (< 30% progress at mid-quarter)
    - Major competitive threat identified
    - Strategic misalignment > 40% of weekly work
    - Resource constraint blocking key initiative

  medium_priority:
    - Weekly strategic alignment < 70%
    - New market opportunity detected
    - Stakeholder request conflicts with strategy

  low_priority:
    - Minor tactical adjustments needed
    - Roadmap optimization suggestions
```

---

## Integration Checklist

### Required Connections
- [ ] Access to company OKR system
- [ ] Product roadmap tool (Jira/Aha/ProductBoard)
- [ ] Calendar integration (Google/Outlook)
- [ ] Task management system (Asana/Notion)
- [ ] Competitive intelligence feeds
- [ ] Document storage (Google Drive/Confluence)

### Data Requirements
- [ ] Current quarter OKRs documented
- [ ] Product vision statement
- [ ] Competitor list and tracking method
- [ ] Strategic initiatives defined
- [ ] Resource capacity baseline

---

## Success Metrics

### Agent Performance KPIs
```yaml
effectiveness:
  - strategic_alignment_score: "> 80%"
  - okr_achievement_rate: "> 70%"
  - roadmap_predictability: "> 85%"

efficiency:
  - time_to_daily_brief: "< 5 min"
  - strategy_prep_time_saved: "> 30%"

quality:
  - decision_quality_score: "> 4/5 (retrospective)"
  - stakeholder_satisfaction: "> 4/5"
```

---

## Customization Options

### Personalization Settings
```yaml
preferences:
  communication_style: [concise/detailed/executive]
  priority_framework: [OKRs/KPIs/Milestones]
  review_frequency: [daily/weekly/biweekly]
  focus_areas: [growth/retention/efficiency/innovation]

industry_context:
  type: [B2B/B2C/Enterprise/SMB]
  vertical: [SaaS/Fintech/Healthcare/etc]
  stage: [Startup/Growth/Mature]
```

---

## Example Usage

### Sample Input (Daily Check)
```
Today's Tasks:
- Review PRD for feature X
- Customer interview for segment Y
- Fix bug in checkout flow
- Team standup
- Stakeholder update meeting

Current OKRs:
O1: Improve user activation by 25%
  KR1: Increase D1 retention from 40% to 50%
  KR2: Reduce time-to-value from 10 min to 5 min
```

### Sample Output
```
## Strategic Alignment Report - 2026-01-01

### Alignment Score: 7/10

### Well-Aligned Tasks:
- Review PRD for feature X → KR2: Time-to-value (onboarding feature)
- Customer interview for segment Y → O1: Understanding activation barriers

### Misaligned Activities:
- Fix bug in checkout flow → Low strategic value
  Recommendation: Delegate to engineer if possible, this is tactical

### Strategic Opportunities Today:
- Customer interview is HIGH VALUE - prepare questions specifically about
  first-session experience and time-to-value
- Stakeholder update: Use this to get buy-in for activation initiatives

### Recommended Adjustments:
1. Dedicate 30 min pre-interview to craft activation-focused questions
2. Delegate bug fix to free up strategic thinking time
3. Add 15 min post-interview to document insights for Discovery Agent
```

---

## Maintenance Schedule

### Weekly
- Review and refine OKR tracking
- Update competitive intelligence sources
- Adjust priority weighting if needed

### Monthly
- Validate strategy alignment metrics
- Update industry/market context
- Refine prompt templates based on feedback

### Quarterly
- Complete agent performance review
- Update integration connections
- Recalibrate success metrics

---

## Notes & Tips

1. **Start Simple**: Begin with just the daily strategy check
2. **Iterate**: Refine prompts based on output quality
3. **Human-in-Loop**: Always review strategic recommendations before acting
4. **Context is Key**: The more context you provide, the better the output
5. **Document Decisions**: Feed strategic decisions back to improve future recommendations
