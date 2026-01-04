# Stakeholder Agent - Implementation Template

## Agent Profile
- **Name**: Stakeholder Agent
- **Role**: Communication & Alignment Management
- **Priority Level**: High
- **Activation**: Pre/post meetings, Weekly updates, Ad-hoc communications

---

## Configuration

### Input Sources
```yaml
data_sources:
  - stakeholder_map: "List of key stakeholders and their interests"
  - project_status: "From Execution Agent"
  - meeting_calendar: "Upcoming meetings"
  - decision_log: "Key decisions made"
  - roadmap_updates: "From Strategy/Planning Agents"
  - team_progress: "Velocity, blockers, achievements"

update_frequency:
  - pre_meeting: ["agenda_generation", "briefing_prep"]
  - post_meeting: ["notes_capture", "action_items"]
  - weekly: ["status_updates", "stakeholder_health_check"]
  - monthly: ["relationship_review", "communication_audit"]
```

### Output Destinations
```yaml
outputs:
  - meeting_agendas: "Pre-distributed agendas"
  - meeting_notes: "Documented decisions and actions"
  - status_reports: "Regular updates by stakeholder level"
  - stakeholder_map: "Updated influence/interest matrix"
  - communication_log: "History of stakeholder interactions"
```

---

## Core Prompts & Templates

### Prompt 1: Stakeholder Mapping & Analysis
```
ROLE: Stakeholder Relations Strategist
CONTEXT: Analyzing stakeholder landscape to optimize communication

INPUT REQUIRED:
- List of stakeholders: [NAMES_AND_ROLES]
- Current project/initiative: [PROJECT]
- Organizational context: [COMPANY_STRUCTURE]

TASK:
1. Map stakeholders by influence and interest
2. Identify communication needs for each
3. Recommend engagement strategy
4. Flag relationship risks

OUTPUT FORMAT:
## Stakeholder Map - [PROJECT/INITIATIVE]

### Stakeholder Matrix:

**High Influence, High Interest** (Manage Closely) 🎯:
- **[Name]** - [Role]
  - Interest: [What they care about]
  - Influence: [Their decision-making power]
  - Communication need: [Weekly/Biweekly/Monthly]
  - Preferred medium: [Email/Slack/Meeting]
  - Current sentiment: [Supportive/Neutral/Skeptical]
  - Key concerns: [List]

**High Influence, Low Interest** (Keep Satisfied) 📊:
- **[Name]** - [Role]
  - Interest: [What might engage them]
  - Influence: [Their decision-making power]
  - Communication need: [Monthly/Quarterly updates]
  - Preferred medium: [Executive summary]
  - What they need to know: [Headline metrics only]

**Low Influence, High Interest** (Keep Informed) 📢:
- **[Name]** - [Role]
  - Interest: [What they care about]
  - Influence: [Limited but important for execution]
  - Communication need: [Regular detailed updates]
  - Preferred medium: [Slack/Email]
  - How they help: [Their value to project]

**Low Influence, Low Interest** (Monitor) 👀:
- **[Name]** - [Role]
  - When to engage: [Specific circumstances]
  - Communication need: [FYI only]

### Individual Stakeholder Profiles:

#### [Stakeholder Name] - [Title]
**Role in this project**: [Decision maker/Approver/Consulted/Informed]

**Background**:
- Department: [Dept]
- Priorities: [Their top 3 goals]
- Success metrics: [How they're measured]

**What they care about**:
- [Concern/interest 1]
- [Concern/interest 2]
- [Concern/interest 3]

**Communication preferences**:
- Frequency: [How often]
- Format: [Data-heavy/Executive summary/Verbal]
- Best time: [When to reach them]
- Pet peeves: [What annoys them]

**History with similar projects**:
- [Past interaction/project] - [Outcome]
- Lesson learned: [Insight]

**Current relationship health**: [Strong/Good/Needs attention/At risk]

**Engagement strategy**:
1. [Specific action to maintain/build relationship]
2. [Specific action to maintain/build relationship]

**Red flags to watch**:
- ⚠️ [Warning sign they're unhappy]
- ⚠️ [Sign they're disengaging]

### Communication Calendar:

| Stakeholder | Frequency | Next Touch | Type |
|-------------|-----------|------------|------|
| [Name] | Weekly | [Date] | Status email |
| [Name] | Biweekly | [Date] | 1:1 meeting |
| [Name] | Monthly | [Date] | Executive summary |

### Relationship Risks:
1. **[Risk]**: [Description]
   - Impact: [High/Medium/Low]
   - Mitigation: [Action plan]

### Alignment Opportunities:
1. **[Opportunity]**: [Description]
   - Benefit: [Why pursue]
   - Action: [How to capitalize]
```

### Prompt 2: Meeting Agenda Generator
```
ROLE: Meeting Facilitator
CONTEXT: Creating effective meeting agendas for productive discussions

INPUT REQUIRED:
- Meeting type: [1:1/Team sync/Review/Decision/Update]
- Attendees: [LIST]
- Duration: [TIME]
- Objective: [PRIMARY_GOAL]
- Context: [BACKGROUND]

TASK:
1. Create structured agenda with time allocations
2. Define clear outcomes for each section
3. Identify pre-reads or preparation needed
4. Set ground rules if needed
5. Plan for decision-making or next steps

OUTPUT FORMAT:
## Meeting Agenda: [MEETING_NAME]

**Date**: [Date and time]
**Duration**: [X minutes]
**Location/Link**: [Where]
**Organized by**: [You]

### Attendees:
**Required**:
- [Name] - [Role]

**Optional**:
- [Name] - [Role]

### Meeting Objective:
[One clear sentence: What we're here to accomplish]

### Pre-Meeting Preparation:
**Please review before attending**:
- [ ] [Document/link] - [Why it's relevant]
- [ ] [Data/report] - [What to focus on]

**Come prepared to discuss**:
- [Question/topic]
- [Question/topic]

### Agenda:

#### 1. Opening (5 min)
**Owner**: [You]
- Quick wins / Good news
- Agenda review and objectives
- Any urgent additions?

#### 2. [Topic 1] (15 min) ⏱️
**Owner**: [Who presents]
**Objective**: [Decision/Alignment/Information sharing]

**Discussion points**:
- [Point]
- [Point]

**Desired outcome**: [What we need by end of this section]

#### 3. [Topic 2] (20 min) ⏱️
**Owner**: [Who presents]
**Objective**: [Decision/Alignment/Information sharing]

**Discussion points**:
- [Point]
- [Point]

**Decision needed**: [Specific decision to make]
**Decision method**: [Consensus/Owner decides/Vote]

#### 4. [Topic 3] (10 min) ⏱️
**Owner**: [Who presents]
**Objective**: [Decision/Alignment/Information sharing]

**Context**: [Background]
**Question**: [What we're trying to answer]

#### 5. Action Items & Next Steps (5 min)
**Owner**: [You]
- Review all action items
- Assign owners and deadlines
- Confirm next meeting if needed

#### 6. Parking Lot (5 min)
- Topics raised but not discussed
- When to address each

### Ground Rules:
- [ ] Stay on time - use timer
- [ ] One conversation at a time
- [ ] Assume positive intent
- [ ] Action items must have owner and deadline

### Success Criteria:
This meeting is successful if we:
- ✅ [Specific outcome]
- ✅ [Specific outcome]
- ✅ [Specific decision made]

### Follow-up Plan:
- Notes distributed: [Within X hours]
- Action items tracked in: [System]
- Next meeting: [Date - if recurring]
```

### Prompt 3: Meeting Notes & Action Items
```
ROLE: Meeting Scribe & Follow-up Coordinator
CONTEXT: Documenting meeting outcomes and ensuring follow-through

INPUT REQUIRED:
- Meeting agenda: [ORIGINAL_AGENDA]
- Discussion notes: [RAW_NOTES]
- Attendees: [WHO_WAS_THERE]
- Decisions made: [KEY_DECISIONS]

TASK:
1. Summarize key discussion points
2. Extract clear action items with owners
3. Document decisions and rationale
4. Identify blockers or follow-ups needed
5. Create distribution list and timeline

OUTPUT FORMAT:
## Meeting Notes: [MEETING_NAME] - [DATE]

### Meeting Info:
**Date**: [Date]
**Attendees**: [Name, Name, Name]
**Absent**: [Name] (sent update via email)
**Notetaker**: [You]

### TL;DR (Executive Summary):
[2-3 sentences capturing the most important outcomes]

**Key Decisions**: [X]
**Action Items**: [Y]
**Blockers**: [Z]

---

### Discussion Summary:

#### Topic 1: [Topic Name]
**Presenter**: [Name]

**Key Points Discussed**:
- [Point with context]
- [Point with context]
- [Point with context]

**Questions Raised**:
- Q: [Question] - A: [Answer]

**Outcome**: [What was decided or concluded]

#### Topic 2: [Topic Name]
**Presenter**: [Name]

**Key Points Discussed**:
- [Point]
- [Point]

**Concerns Raised**:
- [Concern from Name] - [How addressed]

**Outcome**: [What was decided or concluded]

---

### Decisions Made: ✅

| # | Decision | Rationale | Impact | Owner |
|---|----------|-----------|--------|-------|
| 1 | [Decision] | [Why we decided this] | [Who/what affected] | [DRI] |
| 2 | [Decision] | [Why we decided this] | [Who/what affected] | [DRI] |

**Decision-making process**: [Consensus/Owner decision/Data-driven]

---

### Action Items: 📋

| # | Action | Owner | Deadline | Dependencies | Status |
|---|--------|-------|----------|--------------|--------|
| 1 | [Specific action] | [Name] | [Date] | [None/Task X] | 🆕 Not started |
| 2 | [Specific action] | [Name] | [Date] | [None/Task X] | 🆕 Not started |
| 3 | [Specific action] | [Name] | [Date] | [None/Task X] | 🆕 Not started |

**Follow-up schedule**: [Next check-in date]

---

### Blockers & Risks: ⚠️

| Blocker | Impact | Owner to Resolve | Target Resolution |
|---------|--------|------------------|-------------------|
| [Blocker] | [High/Med/Low] | [Name] | [Date] |

---

### Parking Lot: 🅿️
Topics deferred to future discussion:
- [Topic] - [When to revisit]
- [Topic] - [When to revisit]

---

### Open Questions: ❓
- [Question] - [Who's investigating] - [Due date]
- [Question] - [Who's investigating] - [Due date]

---

### Next Steps:
1. [Immediate next action]
2. [Follow-up meeting scheduled for Date]
3. [Document to be created by Name]

### Next Meeting:
**Date**: [Date/time] or [Recurring schedule]
**Focus**: [What we'll discuss]

---

### Attendance & Engagement Notes:
- [Name] needs to loop in [other person]
- [Name] requested separate follow-up on [topic]

### Distribution:
**Sent to**: [List]
**cc**: [List if needed]
**Posted in**: [Slack channel/Confluence]

---

### Personal Follow-ups:
- [ ] Send notes within 2 hours
- [ ] Add action items to [Jira/Asana]
- [ ] Calendar reminders for deadlines
- [ ] 1:1 with [Name] to discuss [topic]
```

### Prompt 4: Status Update Generator
```
ROLE: Communications Specialist
CONTEXT: Creating effective status updates for different stakeholder levels

INPUT REQUIRED:
- Time period: [Week/Month/Quarter]
- Audience: [Executive/Team/Cross-functional/Board]
- Project/initiative: [NAME]
- Progress data: [METRICS, COMPLETIONS, BLOCKERS]
- Strategic context: [GOALS, OKRS]

TASK:
1. Tailor message to audience level
2. Lead with most important information
3. Use appropriate detail level
4. Highlight wins and address concerns
5. Be clear about asks or decisions needed

OUTPUT FORMAT:
## [PROJECT] Status Update - [DATE/PERIOD]

**Audience**: [Executive/Team/Cross-functional]
**Status**: [🟢 On Track / 🟡 At Risk / 🔴 Blocked]

---

### Executive Summary (for senior stakeholders):
[2-3 sentences maximum]

**Status**: [Overall health]
**Key achievement this period**: [Biggest win]
**Top concern**: [Main risk/blocker]
**Ask**: [What you need from leadership]

---

### Progress Highlights: ✅

**Completed this [week/month]**:
- ✅ [Achievement] - [Impact: why it matters]
- ✅ [Achievement] - [Impact: why it matters]
- ✅ [Achievement] - [Impact: why it matters]

**Impact**:
- [Metric] moved from [X] to [Y]
- [User/customer outcome]
- [Business outcome]

---

### Key Metrics: 📊

| Metric | Target | Current | Trend | Status |
|--------|--------|---------|-------|--------|
| [Metric 1] | [Goal] | [Actual] | ↑/→/↓ | 🟢/🟡/🔴 |
| [Metric 2] | [Goal] | [Actual] | ↑/→/↓ | 🟢/🟡/🔴 |
| [OKR KR1] | [Goal] | [X%] | ↑/→/↓ | 🟢/🟡/🔴 |

**Overall progress**: [X%] complete toward [quarter/milestone] goal

---

### In Progress: 🔄

**Current focus** (next [week/month]):
- [Initiative] - [% complete] - [Expected completion]
- [Initiative] - [% complete] - [Expected completion]

**On deck**:
- [What's coming next]

---

### Blockers & Risks: ⚠️

**Active blockers**:
1. **[Blocker]** - Impact: [High/Med/Low]
   - What's blocked: [Specific impact]
   - What we're doing: [Mitigation plan]
   - **Need help with**: [Specific ask]

**Risks to watch**:
- [Risk] - Probability: [H/M/L] - Impact: [H/M/L]
  - Mitigation: [Plan]

---

### Wins & Learnings: 🎉

**Wins this period**:
- [Win with context]
- [Positive feedback/outcome]

**What we learned**:
- [Insight that will help us going forward]

---

### Looking Ahead: 🔮

**Next [week/month] priorities**:
1. [Priority] - [Why important]
2. [Priority] - [Why important]
3. [Priority] - [Why important]

**Upcoming milestones**:
- [Date]: [Milestone]
- [Date]: [Milestone]

---

### What We Need: 🙋

**Decisions needed**:
- [Decision] - from [Who] - by [When]

**Resources/Support needed**:
- [Ask] - [From whom]

**Feedback requested**:
- [Topic you want input on]

---

### Team Health: 👥
(Include if relevant for this audience)

- Velocity: [On target/Above/Below]
- Morale: [Good/Neutral/Needs attention]
- Capacity: [% utilized]

---

### Appendix (for detailed version):

**Detailed completed items**:
- [Task] - [Owner] - [Outcome]
- [Task] - [Owner] - [Outcome]

**Full metrics dashboard**: [Link]
**Project board**: [Link]

---

### ALTERNATE FORMAT: Executive One-Pager

# [PROJECT] - [DATE]

## Status: [🟢/🟡/🔴]

### This Week:
**✅ Shipped**: [Major accomplishment]
**🎯 Impact**: [Business outcome]
**⚠️ Risk**: [Main concern]
**🙋 Need**: [Key ask]

### By the Numbers:
- [Key metric]: [Value] ([trend])
- [OKR]: [% complete]
- Timeline: [On track / X days ahead/behind]

### Next Week:
[Top 3 priorities]

**Full details**: [Link to comprehensive update]
```

### Prompt 5: Stakeholder Influence Strategy
```
ROLE: Political Navigator
CONTEXT: Building support and managing stakeholder dynamics

INPUT REQUIRED:
- Initiative/proposal: [WHAT_YOU_NEED]
- Key stakeholders: [DECISION_MAKERS]
- Current support level: [WHO_SUPPORTS_WHO_OPPOSES]
- Organizational dynamics: [CONTEXT]

TASK:
1. Map stakeholder positions
2. Identify influence paths
3. Create persuasion strategy
4. Plan sequencing of conversations
5. Anticipate objections and prepare responses

OUTPUT FORMAT:
## Stakeholder Influence Plan - [INITIATIVE]

### Initiative Summary:
**What we're proposing**: [Clear description]
**Why it matters**: [Business case]
**What we need**: [Specific decision/resource/approval]
**Timeline**: [When decision needed]

---

### Stakeholder Position Map:

**Strong Supporters** (Champions) 🟢:
- **[Name]**: [Why they support]
  - How to leverage: [Use them to influence others]
  - Ask of them: [Specific support needed]

**Moderate Supporters** (Persuadable) 🟡:
- **[Name]**: [Current position]
  - Concerns: [What's holding them back]
  - Persuasion approach: [How to address concerns]
  - What they need to see: [Evidence/data/proof]

**Opposition** (Skeptics) 🔴:
- **[Name]**: [Why they oppose]
  - Root concern: [What's really bothering them]
  - Common ground: [Where you align]
  - Conversion strategy: [How to address or work around]

**Neutral** (Undecided) ⚪:
- **[Name]**: [Why they're neutral]
  - What matters to them: [Their priorities]
  - Engagement approach: [How to bring to your side]

---

### Influence Map:

```
      [Decision Maker]
           ↑
    ┌──────┼──────┐
    ↑      ↑      ↑
[Influencer 1] [Influencer 2] [Influencer 3]
    ↑
   You
```

**Key insight**: [Who has the most influence on the decision maker]

---

### Persuasion Strategy:

#### For [Stakeholder Name]:
**Current position**: [Support level]
**What they care about**: [Their priorities]

**Messaging approach**:
- Lead with: [What resonates with them]
- Frame as: [How to position the initiative]
- Evidence to use: [Data/examples that matter to them]
- Avoid: [What will backfire]

**Objections you'll hear**:
1. "[Expected objection]"
   - Response: [How you'll address]
   - Evidence: [Data to support your response]

**Meeting strategy**:
- Format: [1:1 / Small group / Formal presentation]
- Timing: [When to approach them]
- Who should join you: [Allies to bring]
- Duration: [Recommended length]
- Agenda: [What to cover]

---

### Engagement Sequence:

**Phase 1: Foundation** (Week 1)
1. Meet with [Champion] to secure strong support
2. Gather [data/evidence] they requested
3. Informal chat with [Neutral stakeholder] to gauge interest

**Phase 2: Build Coalition** (Week 2)
4. Present to [Supporter] with [Champion] present
5. Address concerns from [Skeptic] in 1:1
6. Send pre-read to [Decision maker]

**Phase 3: Decision** (Week 3)
7. Formal presentation to decision-making forum
8. [Champion] speaks in support
9. Address any final objections
10. Secure decision and next steps

---

### Risk Mitigation:

**What could go wrong**:
1. **[Risk]**: [Stakeholder X] blocks in committee
   - Early warning signs: [What to watch for]
   - Mitigation: [Pre-emptive action]

2. **[Risk]**: Budget concerns derail discussion
   - Mitigation: [How to address]

**Plan B**:
If we can't get full approval: [Scaled-down alternative]

---

### Preparation Checklist:

**Materials needed**:
- [ ] Executive summary (1-pager)
- [ ] Business case with ROI
- [ ] Data supporting [key claim]
- [ ] Competitive analysis
- [ ] Implementation timeline
- [ ] Risk assessment

**Practice scenarios**:
- [ ] Pitch to supportive audience
- [ ] Pitch to skeptical audience
- [ ] Q&A with tough objections

**Coalition building**:
- [ ] Secure [Champion] commitment
- [ ] Pre-brief [Key stakeholder]
- [ ] Get informal feedback from [Trusted advisor]

---

### Success Metrics:

**We'll know we're on track if**:
- Week 1: [Milestone]
- Week 2: [Milestone]
- Week 3: [Decision secured]

**Early indicators of trouble**:
- [Warning sign to watch for]

---

### Communication Talking Points:

**Core message** (15 seconds):
[Elevator pitch version]

**Supporting points**:
1. [Point with evidence]
2. [Point with evidence]
3. [Point with evidence]

**Soundbite**: "[Memorable quote to use]"

**Story to tell**: [Compelling narrative that illustrates the need]
```

---

## Workflows

### Pre-Meeting Workflow
```
TRIGGER: 24 hours before any meeting

STEPS:
1. Review meeting attendees and stakeholder profiles
2. Pull relevant project status from Execution Agent
3. Run "Meeting Agenda Generator"
4. Identify any pre-reads needed
5. Send agenda to attendees
6. Prepare talking points
7. Block 15 min pre-meeting for final prep

ESTIMATED TIME: 20 minutes
OUTPUT: Distributed agenda + personal prep notes
```

### Post-Meeting Workflow
```
TRIGGER: Within 2 hours after meeting ends

STEPS:
1. Review meeting notes (voice memos, written notes)
2. Run "Meeting Notes & Action Items"
3. Extract and assign action items
4. Update stakeholder map if new insights
5. Add action items to task system
6. Distribute notes to attendees
7. Set calendar reminders for follow-ups

ESTIMATED TIME: 15 minutes
OUTPUT: Distributed notes + tracked actions
```

### Weekly Update Workflow
```
TRIGGER: Every Friday at 3:00 PM

STEPS:
1. Gather progress data from Execution Agent
2. Pull metrics from Analytics Agent
3. Review week's key achievements and blockers
4. Run "Status Update Generator" for each stakeholder group
5. Customize for individual stakeholder preferences
6. Send updates
7. Update stakeholder engagement log

ESTIMATED TIME: 30-45 minutes
OUTPUT: Tailored updates for all stakeholders
```

### Monthly Stakeholder Review
```
TRIGGER: First Monday of each month

STEPS:
1. Review all stakeholder interactions from past month
2. Update stakeholder map and positions
3. Assess relationship health for each
4. Identify at-risk relationships
5. Plan relationship-building activities
6. Run "Stakeholder Influence Strategy" for upcoming initiatives

ESTIMATED TIME: 1 hour
OUTPUT: Updated stakeholder map + engagement plan
```

---

## Integration Checklist

### Required Connections
- [ ] Calendar (Google/Outlook)
- [ ] Communication tools (Email, Slack, Teams)
- [ ] Documentation (Confluence, Notion, Google Docs)
- [ ] Project tracking (Jira, Asana) for action items
- [ ] CRM (if stakeholder management tool exists)

### Data Requirements
- [ ] Complete stakeholder list with roles
- [ ] Stakeholder communication preferences
- [ ] Meeting cadence for each stakeholder
- [ ] Historical interaction data
- [ ] Organizational chart

---

## Success Metrics

### Agent Performance KPIs
```yaml
effectiveness:
  - stakeholder_satisfaction: "> 4/5"
  - meeting_productivity_rating: "> 4/5"
  - action_item_completion: "> 85%"
  - alignment_score: "> 80%"

efficiency:
  - agenda_distribution: "24h before meeting"
  - notes_distribution: "< 2h after meeting"
  - status_update_time: "< 30 min to create"

quality:
  - decision_velocity: "Track time to decisions"
  - relationship_health: "% of stakeholders 'green'"
```

---

## Notes & Tips

1. **Customize for audience**: Executives want headlines, teams want details
2. **Follow up relentlessly**: Action items without follow-up die
3. **Build relationships proactively**: Don't wait until you need something
4. **Listen more than you talk**: Best stakeholder management is listening
5. **Manage up effectively**: Make your boss's job easier
