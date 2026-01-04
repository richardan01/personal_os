# Discovery Agent - Implementation Template

## Agent Profile
- **Name**: Discovery Agent
- **Role**: User Research & Requirements Gathering
- **Priority Level**: High
- **Activation**: Continuous (processes feedback as it arrives)

---

## Configuration

### Input Sources
```yaml
data_sources:
  - user_interviews: "Interview transcripts/notes"
  - support_tickets: "Zendesk/Intercom"
  - feature_requests: "ProductBoard/Canny"
  - user_analytics: "Mixpanel/Amplitude events"
  - sales_feedback: "CRM notes, Gong calls"
  - nps_surveys: "Survey responses"
  - social_listening: "Twitter/Reddit mentions"

update_frequency:
  - real_time: ["urgent_feedback", "critical_bugs"]
  - daily: ["feedback_synthesis", "trend_detection"]
  - weekly: ["insight_report", "persona_updates"]
```

### Output Destinations
```yaml
outputs:
  - insight_database: "Centralized research repository"
  - feature_requests: "Prioritized request backlog"
  - user_personas: "Living persona documents"
  - research_reports: "Weekly synthesis reports"
  - planning_agent_feed: "Requirements for Planning Agent"
```

---

## Core Prompts & Templates

### Prompt 1: Interview Notes Synthesizer
```
ROLE: User Research Analyst
CONTEXT: Analyzing user interview to extract actionable insights

INPUT REQUIRED:
- Interview transcript/notes: [TRANSCRIPT]
- Interviewee profile: [NAME, ROLE, COMPANY/SEGMENT]
- Interview objective: [RESEARCH_GOAL]
- Current product context: [CONTEXT]

TASK:
1. Extract key pain points mentioned
2. Identify jobs-to-be-done
3. Capture memorable quotes (verbatim)
4. Note feature requests or suggestions
5. Identify patterns with previous interviews
6. Rate urgency and impact of feedback

OUTPUT FORMAT:
## Interview Synthesis - [INTERVIEWEE] - [DATE]

### Profile:
- **Name**: [Name/Anonymous ID]
- **Role**: [Title]
- **Company/Segment**: [Details]
- **User Type**: [Power User/New User/Churned/etc]

### Key Pain Points:
1. **[Pain Point]**
   - Severity: [High/Medium/Low]
   - Frequency: [How often encountered]
   - Impact: [Business/workflow impact]
   - Quote: "[Exact words]"

### Jobs-to-be-Done:
- **Functional Job**: [What they're trying to accomplish]
- **Emotional Job**: [How they want to feel]
- **Social Job**: [How they want to be perceived]

### Notable Quotes:
> "[Powerful quote 1]"
> "[Powerful quote 2]"

### Feature Requests:
| Request | Priority | Workaround Exists? | Urgency |
|---------|----------|-------------------|---------|
| [Request] | [H/M/L] | [Yes/No] | [Days/Weeks/Months] |

### Patterns Detected:
- This is the [Nth] time we've heard about [issue]
- Connects to previous feedback from [segment/user]
- New insight: [Something we haven't heard before]

### Recommended Actions:
1. [Immediate action] - [Why]
2. [Short-term action] - [Why]
3. [Long-term consideration] - [Why]

### Tags:
#[segment] #[feature-area] #[pain-point-category]
```

### Prompt 2: Feature Request Analyzer
```
ROLE: Product Requirements Analyst
CONTEXT: Processing incoming feature requests to understand true needs

INPUT REQUIRED:
- Feature request: [REQUEST_DESCRIPTION]
- Requester info: [WHO, SEGMENT, CONTEXT]
- Similar requests: [EXISTING_REQUESTS]

TASK:
1. Identify the underlying need (not just the solution requested)
2. Categorize the request
3. Assess priority using impact/effort framework
4. Link to existing requests or roadmap items
5. Recommend next steps

OUTPUT FORMAT:
## Feature Request Analysis - [REQUEST_ID]

### Request Summary:
**Original Request**: [What user asked for]
**Submitted By**: [User/Segment]
**Date**: [Date]

### Underlying Need:
**What they really need**: [The actual problem to solve]
**Why**: [Root cause analysis]
**Current workaround**: [How they solve it today]

### Categorization:
- **Type**: [New Feature/Enhancement/Fix/Integration]
- **Product Area**: [Which module/feature]
- **User Segment**: [Who needs this]
- **Use Case**: [When/why they need it]

### Impact Assessment:
- **Reach**: [How many users affected] - Score: [1-10]
- **Impact**: [How much it helps] - Score: [1-10]
- **Confidence**: [How sure are we] - Score: [1-10]
- **Effort**: [Time to build] - Score: [1-10]
- **RICE Score**: [Calculated score]

### Similar Requests:
- [Request #X]: [Similar because...] - [Count: X users]
- Total requesting this: [N users/companies]

### Business Value:
- **Revenue Impact**: [Potential ARR/upsell]
- **Retention Impact**: [Churn risk if not built]
- **Competitive**: [Do competitors have this?]

### Recommendation:
**Priority**: [Critical/High/Medium/Low/Declined]
**Status**: [Add to backlog/Merge with existing/Needs more research/Decline]
**Next Steps**:
1. [Action item]
2. [Action item]

### Response to User:
[Draft message acknowledging request and setting expectations]
```

### Prompt 3: Feedback Trend Detector
```
ROLE: Pattern Recognition Analyst
CONTEXT: Identifying emerging trends across all feedback sources

INPUT REQUIRED:
- Feedback from last [7/30] days: [FEEDBACK_COLLECTION]
- Previous trends: [HISTORICAL_TRENDS]
- Product changes: [RECENT_RELEASES]

TASK:
1. Identify recurring themes
2. Detect sentiment shifts
3. Correlate with product changes
4. Flag emerging issues
5. Highlight positive feedback trends

OUTPUT FORMAT:
## Feedback Trends Report - [DATE_RANGE]

### Executive Summary:
[2-3 sentence overview of key findings]

### Top Themes (by mention volume):
1. **[Theme]** - [X mentions, +/-% vs last period]
   - Sentiment: [Positive/Negative/Mixed]
   - Segments affected: [List]
   - Example: "[Quote]"
   - Action needed: [Yes/No - What]

### Emerging Issues (⚠️ New or Growing):
- **[Issue]**: [Description]
  - First seen: [Date]
  - Growth rate: [X% increase]
  - Potential impact: [High/Med/Low]
  - Recommended action: [Action]

### Positive Signals (✅):
- **[What users love]**: [X mentions]
  - Why it matters: [Strategic value]
  - Opportunity: [How to amplify]

### Sentiment Analysis:
```
Overall NPS/CSAT trend: [↑/↓/→]
Promoters: [X%] (↑/↓ [X%])
Passives: [X%] (↑/↓ [X%])
Detractors: [X%] (↑/↓ [X%])
```

### Correlations with Product Changes:
- **[Release/Change]**:
  - Feedback volume: [X mentions]
  - Sentiment: [Positive/Negative]
  - Unexpected impact: [Description]

### Strategic Insights:
1. [Insight] - [Why it matters for strategy]
2. [Insight] - [Why it matters for strategy]

### Recommended Actions:
**Immediate** (This week):
- [Action]

**Short-term** (This month):
- [Action]

**Strategic** (This quarter):
- [Action]
```

### Prompt 4: User Persona Generator
```
ROLE: User Research Strategist
CONTEXT: Creating or updating user personas based on research data

INPUT REQUIRED:
- Research data: [INTERVIEWS, SURVEYS, ANALYTICS]
- User segments: [IDENTIFIED_SEGMENTS]
- Behavioral data: [USAGE_PATTERNS]

TASK:
1. Synthesize data into coherent persona
2. Include demographic and psychographic info
3. Define goals, pain points, and behaviors
4. Create realistic narrative
5. Link to product implications

OUTPUT FORMAT:
## User Persona: [PERSONA_NAME]

### Overview:
**Archetype**: [Descriptive title]
**Segment Size**: [% of user base or X companies]
**Value to Business**: [High/Medium/Low - Why]

### Demographics:
- **Role/Title**: [Job title]
- **Company Size**: [Enterprise/Mid-market/SMB]
- **Industry**: [Primary industries]
- **Experience Level**: [Beginner/Intermediate/Expert]
- **Team Size**: [How many on their team]

### Psychographics:
- **Tech Savviness**: [Low/Medium/High]
- **Risk Tolerance**: [Conservative/Moderate/Innovative]
- **Decision Style**: [Data-driven/Intuitive/Collaborative]
- **Working Style**: [Structured/Flexible/Chaotic]

### Background & Context:
[2-3 paragraph narrative describing their typical day, challenges, environment]

### Goals & Motivations:
**Primary Goals**:
1. [Goal] - [Why it matters to them]
2. [Goal] - [Why it matters to them]

**Success Metrics** (How they measure themselves):
- [Metric]
- [Metric]

### Pain Points & Frustrations:
1. **[Pain Point]**
   - Impact: [How it affects their work]
   - Current solution: [How they cope]
   - Quote: "[Real user quote]"

### Jobs-to-be-Done:
When ___[situation]___, I want to ___[motivation]___, so I can ___[outcome]___.

### Behaviors & Usage Patterns:
- **Login Frequency**: [Daily/Weekly/Monthly]
- **Session Duration**: [Average time]
- **Peak Usage Times**: [When they use product]
- **Key Features Used**: [Top 3-5 features]
- **Collaboration**: [Solo/Team-based usage]

### Technology Stack:
- [Tool they use]
- [Tool they use]
- [Tool they integrate with]

### Buying Journey:
- **Awareness**: [How they discover solutions]
- **Consideration**: [What they evaluate]
- **Decision Criteria**: [Top 3 factors]
- **Influencers**: [Who else is involved]

### Quotes:
> "[Representative quote about goals]"
> "[Representative quote about pain points]"
> "[Representative quote about our product]"

### Product Implications:
**What this persona needs**:
- [Feature/capability]
- [Feature/capability]

**What to avoid**:
- [Anti-pattern that frustrates them]

**Communication preferences**:
- [How they want to be reached]
- [Tone and style that resonates]

### Journey Map Touchpoints:
1. **Onboarding**: [Specific needs]
2. **Regular Use**: [Specific needs]
3. **Advanced Use**: [Specific needs]
4. **Renewal**: [Specific needs]

---

**Last Updated**: [Date]
**Based On**: [X interviews, Y surveys, Z data points]
**Confidence Level**: [High/Medium/Low]
```

### Prompt 5: Problem Validation Framework
```
ROLE: Product Discovery Specialist
CONTEXT: Validating whether a problem is worth solving

INPUT REQUIRED:
- Problem statement: [PROBLEM]
- User feedback: [EVIDENCE]
- Segment: [WHO_HAS_THIS]

TASK:
1. Assess problem severity and frequency
2. Validate with evidence
3. Quantify opportunity
4. Recommend validation approach

OUTPUT FORMAT:
## Problem Validation - [PROBLEM_NAME]

### Problem Statement:
[One clear sentence describing the problem]

### Evidence:
- **Direct mentions**: [X users/companies]
- **Indirect signals**: [Support tickets, workarounds, etc.]
- **Interview quotes**: "[Quote]"
- **Quantitative data**: [Analytics showing the issue]

### Severity Assessment:
**Impact**: [Critical/High/Medium/Low]
- [Description of impact on user's work/business]

**Frequency**: [Constant/Daily/Weekly/Rare]
- [How often users encounter this]

**Segments Affected**:
- [Segment 1]: [X% of users]
- [Segment 2]: [Y% of users]

### Opportunity Sizing:
**Market Size**: [TAM of users with this problem]
**Revenue Potential**: [ARR impact if solved]
**Retention Risk**: [Churn risk if unsolved]
**Competitive Advantage**: [High/Medium/Low]

### Current State:
**How users solve it today**:
- [Workaround 1]
- [Workaround 2]

**Pain level of workaround**: [1-10]

### Validation Status:
**Confidence**: [High/Medium/Low]
**What we know**: [List validated facts]
**What we assume**: [List assumptions]
**What we need to learn**: [Open questions]

### Recommended Next Steps:
**If confidence is HIGH**:
- Proceed to solution exploration
- Priority: [High/Medium/Low]

**If confidence is MEDIUM/LOW**:
1. [Validation activity needed]
2. [Additional research required]
3. [Experiment to run]

### Success Criteria (for solution):
If we solve this, we should see:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [User sentiment change]
```

---

## Workflows

### Continuous Workflow: Feedback Intake
```
TRIGGER: New feedback received (any source)

STEPS:
1. Capture raw feedback with metadata
2. Run initial categorization
3. Check for critical/urgent flags
4. Link to existing themes or create new
5. Update trend counters
6. Alert if threshold reached (e.g., 5 mentions of same issue)

ESTIMATED TIME: < 1 minute per item
```

### Daily Workflow: Feedback Digest
```
TRIGGER: Every weekday at 5:00 PM

STEPS:
1. Aggregate all feedback from past 24 hours
2. Run "Feedback Trend Detector" on daily data
3. Highlight any urgent items
4. Update running weekly trends
5. Generate daily summary
6. Send to Discovery log

ESTIMATED TIME: 10 minutes
```

### Weekly Workflow: Research Synthesis
```
TRIGGER: Every Friday at 2:00 PM

STEPS:
1. Run "Feedback Trend Detector" on weekly data
2. Synthesize all interviews from the week
3. Update persona documents if new insights
4. Generate top 10 feature requests (by RICE)
5. Create weekly insight report
6. Prepare research highlights for Monday team meeting

ESTIMATED TIME: 45 minutes
```

### Monthly Workflow: Deep Discovery Review
```
TRIGGER: Last Friday of each month

STEPS:
1. Comprehensive trend analysis (full month)
2. Persona refresh and validation
3. Problem validation for top themes
4. Research roadmap for next month
5. Strategic insight report for leadership
6. Update discovery metrics dashboard

ESTIMATED TIME: 2-3 hours
```

---

## Decision Framework

### When to Escalate/Alert
```yaml
alert_conditions:
  critical:
    - Same critical issue mentioned by 5+ users in 48 hours
    - Churning customer mentions specific blocker
    - Security/privacy concern raised
    - Competitor feature causing defection

  high_priority:
    - Enterprise customer feature request
    - Consistent theme across 10+ feedback items
    - NPS detractor pattern detected
    - Positive feedback spike (opportunity)

  medium_priority:
    - New pain point category emerging
    - Feature request from power users
    - Usability issue reported 3+ times
```

---

## Integration Checklist

### Required Connections
- [ ] Customer support platform (Zendesk/Intercom)
- [ ] Feature request tool (ProductBoard/Canny)
- [ ] Analytics platform (Mixpanel/Amplitude)
- [ ] CRM system (Salesforce/HubSpot)
- [ ] Survey tools (Typeform/SurveyMonkey)
- [ ] Interview note storage (Notion/Dovetail/Google Docs)
- [ ] Slack (for alerts)

### Data Requirements
- [ ] User segmentation defined
- [ ] Feedback categorization taxonomy
- [ ] Interview template
- [ ] Feature request intake form
- [ ] Baseline personas (if existing)

---

## Success Metrics

### Agent Performance KPIs
```yaml
effectiveness:
  - feedback_processing_rate: "100% within 24 hours"
  - insight_to_action_time: "< 1 week"
  - persona_accuracy: "> 85% (validated quarterly)"

efficiency:
  - time_to_synthesize_interview: "< 15 min"
  - feedback_categorization_accuracy: "> 90%"

quality:
  - feature_validation_success_rate: "> 70%"
  - research_impact_on_decisions: "Track usage in PRDs"
```

---

## Customization Options

### Personalization Settings
```yaml
preferences:
  detail_level: [executive_summary/detailed/comprehensive]
  focus_areas: [pain_points/feature_requests/opportunities]
  segment_priority: [enterprise/smb/all_equal]
  alert_threshold: [conservative/moderate/aggressive]

research_methods:
  primary: [interviews/surveys/both]
  validation_rigor: [high/medium/pragmatic]
  synthesis_style: [quantitative/qualitative/mixed]
```

---

## Example Usage

### Sample Input (Interview)
```
Interview with Sarah, Product Manager at TechCorp
Date: 2026-01-01
Duration: 30 minutes

Notes:
- Frustrated with current reporting - takes 2 hours to compile weekly report
- Uses 3 different tools to get all data
- Wishes she could just click button and get report
- Team of 5 PMs all have same problem
- Currently paying for separate reporting tool ($500/mo)
- Would pay more for our product if it had this
- "I waste half a day every week just copy-pasting data"
```

### Sample Output
```
## Interview Synthesis - Sarah (TechCorp) - 2026-01-01

### Profile:
- **Role**: Product Manager
- **Company**: TechCorp (Mid-market SaaS)
- **User Type**: Power User (daily active)

### Key Pain Points:
1. **Manual Report Compilation**
   - Severity: HIGH
   - Frequency: Weekly (2 hours lost)
   - Impact: 10% of work week wasted on manual tasks
   - Quote: "I waste half a day every week just copy-pasting data"

### Jobs-to-be-Done:
- **Functional**: Quickly share product metrics with stakeholders
- **Emotional**: Feel efficient and in control
- **Social**: Be seen as data-driven and organized

### Feature Requests:
| Request | Priority | Workaround? | Urgency |
|---------|----------|-------------|---------|
| One-click reporting | HIGH | 3 tools + manual | 2 weeks |

### Patterns Detected:
- This is the 12th mention of reporting pain points
- Mid-market segment specifically struggling (6 mentions)
- Similar to Enterprise request from last month

### Recommended Actions:
1. IMMEDIATE: Check if other TechCorp users have same issue
2. SHORT-TERM: Validate reporting requirements across segment
3. LONG-TERM: Add reporting feature to roadmap for Q2

### Tags:
#mid-market #reporting #efficiency #power-user
```

---

## Maintenance Schedule

### Daily
- Review feedback processing accuracy
- Adjust categorization rules as needed

### Weekly
- Validate trend detection quality
- Update synthesis templates based on feedback

### Monthly
- Review persona accuracy
- Refine RICE scoring calibration
- Update integration connections

---

## Notes & Tips

1. **Capture context**: Always note user segment, role, and product usage level
2. **Verbatim quotes**: Keep exact wording - powerful for stakeholder buy-in
3. **Look for patterns**: One user's pain point is feedback; ten users' is a trend
4. **Validate early**: Don't wait for perfect data - test assumptions quickly
5. **Close the loop**: Always respond to users who give feedback
