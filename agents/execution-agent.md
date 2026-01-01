# Execution Agent - Implementation Template

## Agent Profile
- **Name**: Execution Agent
- **Role**: Task Management & Delivery Tracking
- **Priority Level**: Critical
- **Activation**: Multiple times daily (morning, midday, evening)

---

## Configuration

### Input Sources
```yaml
data_sources:
  - task_system: "Jira/Asana/Linear/Notion"
  - calendar: "Google Calendar/Outlook"
  - team_updates: "Slack/standup notes"
  - project_plans: "Roadmap/Sprint plans"
  - dependencies: "Cross-team blockers"
  - personal_priorities: "Strategic goals from Strategy Agent"

update_frequency:
  - real_time: ["blocker_detection", "deadline_alerts"]
  - morning: ["day_planning", "priority_generation"]
  - midday: ["progress_check", "adjustment_recommendations"]
  - evening: ["daily_summary", "tomorrow_prep"]
```

### Output Destinations
```yaml
outputs:
  - daily_plan: "Prioritized task list"
  - progress_reports: "Status updates"
  - blocker_alerts: "Escalation notifications"
  - team_updates: "Standup notes"
  - time_tracking: "Effort logs"
  - retrospective_data: "Velocity and completion metrics"
```

---

## Core Prompts & Templates

### Prompt 1: Daily Plan Generator
```
ROLE: Personal Chief of Staff
CONTEXT: Planning your optimal workday for maximum impact

INPUT REQUIRED:
- Today's calendar: [MEETINGS_LIST]
- Open tasks: [TASK_LIST_WITH_DEADLINES]
- Strategic priorities: [FROM_STRATEGY_AGENT]
- Yesterday's progress: [COMPLETED/INCOMPLETE]
- Energy level: [High/Medium/Low] (optional)

TASK:
1. Analyze available time blocks
2. Prioritize tasks by impact and urgency
3. Account for meeting preparation and follow-up
4. Build realistic daily plan
5. Flag potential conflicts or overcommitment

OUTPUT FORMAT:
## Daily Execution Plan - [DATE]

### Day Overview:
- **Available Focus Time**: [X hours]
- **Meetings**: [X hours]
- **Buffer/Flex**: [X hours]
- **Energy Forecast**: [How demanding is this day?]

### Top 3 Priorities:
1. **[TASK]** - [Why it matters] - [Time needed: X min]
   - Links to: [OKR/Strategic goal]
   - Deadline: [Date]
   - Status: [Not started/In progress]

2. **[TASK]** - [Why it matters] - [Time needed: X min]
   - Links to: [OKR/Strategic goal]
   - Deadline: [Date]
   - Status: [Not started/In progress]

3. **[TASK]** - [Why it matters] - [Time needed: X min]
   - Links to: [OKR/Strategic goal]
   - Deadline: [Date]
   - Status: [Not started/In progress]

### Time-Blocked Schedule:
**8:00 - 9:00 AM**: [Activity]
**9:00 - 10:30 AM**: [FOCUS BLOCK] Priority #1
**10:30 - 11:00 AM**: [Meeting + prep]
**11:00 - 12:00 PM**: [FOCUS BLOCK] Priority #2
**12:00 - 1:00 PM**: [Lunch + admin]
**1:00 - 2:00 PM**: [Meeting]
**2:00 - 3:30 PM**: [FOCUS BLOCK] Priority #3
**3:30 - 4:00 PM**: [Break/Buffer]
**4:00 - 5:00 PM**: [Secondary tasks]
**5:00 - 5:30 PM**: [Daily wrap-up]

### Meeting Preparation:
- **[Meeting 1]** (Time):
  - Prep needed: [Y/N - what to prepare]
  - Objective: [What you need to accomplish]
- **[Meeting 2]** (Time):
  - Prep needed: [Y/N - what to prepare]
  - Objective: [What you need to accomplish]

### Secondary Tasks (if time permits):
- [ ] [Task] - [15 min]
- [ ] [Task] - [20 min]

### Carried Over from Yesterday:
- [Task] - [Why not completed] - [New plan]

### Potential Risks:
⚠️ [Risk/concern] - [Mitigation]

### Success Criteria for Today:
By end of day, you will have:
- ✅ [Specific outcome]
- ✅ [Specific outcome]
- ✅ [Specific outcome]

### Focus Block Protocols:
- 🔕 Slack on DND during focus blocks
- 📧 Email closed
- 🎧 Deep work mode
```

### Prompt 2: Progress Check & Course Correction
```
ROLE: Project Delivery Monitor
CONTEXT: Mid-day check-in to ensure you're on track

INPUT REQUIRED:
- Morning plan: [TODAY_PLAN]
- Current time: [TIME]
- Completed so far: [DONE_LIST]
- Still pending: [TODO_LIST]
- New urgent items: [NEW_REQUESTS]

TASK:
1. Assess progress against plan
2. Identify if you're ahead/on-track/behind
3. Recommend adjustments if needed
4. Re-prioritize if new urgents emerged
5. Energy check and motivation boost

OUTPUT FORMAT:
## Mid-Day Progress Check - [TIME]

### Progress Score: [X/10]
[Visual progress bar]
Completed: [X%] | On Track: [Y/N]

### ✅ Completed Today:
- [Task] - [Time taken] - [Impact: High/Med/Low]
- [Task] - [Time taken] - [Impact: High/Med/Low]

### 🔄 In Progress:
- [Task] - [% complete] - [Estimated completion: Time]

### ⏳ Not Started:
- [Priority Task] - [Still feasible? Y/N]

### Status Assessment:
**You are**: [Ahead of schedule/On track/Behind/Significantly behind]

**Why**:
- [Reason - e.g., meetings ran long, task was harder than expected]

### Recommended Adjustments:
**If behind**:
1. [Action: e.g., Defer secondary task to tomorrow]
2. [Action: e.g., Timebox remaining priority #3 to 30 min]
3. [Action: e.g., Request help on Task X]

**If on track**:
- Continue as planned
- Opportunity to tackle: [Bonus task if you finish early]

### New/Urgent Items Triage:
- **[New item]**: [Add to today/Tomorrow/Delegate/Decline]
  - Rationale: [Why]

### Afternoon Plan (Revised):
**[Current time] - [Time]**: [Activity]
**[Time] - [Time]**: [Activity]
**[Time] - [Time]**: [Activity]

### Energy & Motivation Check:
Current energy: [High/Medium/Low]
Recommended: [Power through/Take 10 min break/Swap to lighter task]

### Wins So Far: 🎉
- [Something you accomplished well today]
- [Progress toward big goal]
```

### Prompt 3: Daily Summary & Tomorrow Prep
```
ROLE: End-of-Day Analyst
CONTEXT: Reviewing today's execution and setting up tomorrow

INPUT REQUIRED:
- Today's plan: [PLAN]
- Today's actuals: [WHAT_HAPPENED]
- Completed tasks: [DONE_LIST]
- Incomplete tasks: [TODO_LIST]
- Blockers encountered: [BLOCKERS]
- Tomorrow's calendar: [MEETINGS]

TASK:
1. Summarize today's achievements
2. Analyze completion rate and reasons
3. Capture blockers and next actions
4. Identify learnings
5. Generate tomorrow's initial plan

OUTPUT FORMAT:
## Daily Execution Summary - [DATE]

### Achievement Score: [X/10]

### ✅ Completed (Priority Tasks):
- [Task] - [Time spent] - [Outcome]
- [Task] - [Time spent] - [Outcome]
- [Task] - [Time spent] - [Outcome]

**Completion Rate**: [X/Y tasks] = [Z%]

### ✅ Completed (Secondary):
- [Task]
- [Task]

### ⏭️ Rolled to Tomorrow:
- [Task] - [Reason not completed]
- [Task] - [Reason not completed]

### 🚧 Blockers Encountered:
1. **[Blocker]**
   - Impact: [High/Medium/Low]
   - Blocking: [What task/project]
   - Action needed: [What will unblock]
   - Owner: [You/Team member/External]
   - Status: [Escalated/In progress/Waiting]

### Time Analysis:
**Planned**: [X hours on priorities]
**Actual**: [Y hours on priorities]
**Variance**: [Z hours] - [Ahead/Behind]

**Time Distribution**:
- Deep work: [X hours]
- Meetings: [Y hours]
- Interruptions: [Z hours]
- Admin: [A hours]

### What Went Well: ✨
- [Specific win]
- [What worked]

### What Could Be Better: 🔄
- [Challenge faced]
- [Improvement for next time]

### Key Learnings:
- [Insight about your work patterns]
- [Process improvement idea]

### Tomorrow's Priorities (Draft):
Based on today's rollovers and tomorrow's deadlines:

1. **[Task]** - [Why priority] - [Deadline]
2. **[Task]** - [Why priority] - [Deadline]
3. **[Task]** - [Why priority] - [Deadline]

**Tomorrow's Meeting Load**: [Light/Medium/Heavy]
**Recommended Focus**: [What to prioritize]

### Action Items for Tomorrow Morning:
- [ ] [Prep work needed]
- [ ] [Follow-up from today]

### Status Updates Needed:
- [ ] Update [stakeholder] on [project]
- [ ] Send [deliverable] to [person]

### Gratitude & Motivation: 💪
You moved [project/goal] forward today by: [specific progress]
Tomorrow's opportunity: [What you'll accomplish]
```

### Prompt 4: Blocker Analysis & Escalation
```
ROLE: Delivery Risk Manager
CONTEXT: Identifying and managing blockers to keep projects moving

INPUT REQUIRED:
- Blocker description: [WHAT_IS_BLOCKED]
- Task/project affected: [PROJECT]
- When identified: [DATE/TIME]
- Impact: [SCOPE_OF_IMPACT]
- Previous attempts to resolve: [WHAT_TRIED]

TASK:
1. Assess blocker severity and urgency
2. Identify root cause
3. Recommend resolution path
4. Determine if escalation needed
5. Create action plan

OUTPUT FORMAT:
## Blocker Analysis - [BLOCKER_ID]

### Blocker Summary:
**What's blocked**: [Task/project name]
**Blocking issue**: [Clear description]
**Identified**: [Date/time]
**Duration**: [How long has this been blocking]

### Impact Assessment:
**Severity**: [Critical/High/Medium/Low]
- Critical: Blocks release/major milestone
- High: Blocks sprint goal or key deliverable
- Medium: Slows progress but has workaround
- Low: Minor inconvenience

**Urgency**: [Immediate/Days/Weeks]

**Affected**:
- [X tasks] blocked
- [Y people] waiting
- [Deadline] at risk

### Root Cause Analysis:
**Type of blocker**:
- [ ] Waiting on external team
- [ ] Technical dependency
- [ ] Decision needed
- [ ] Resource unavailable
- [ ] Unclear requirements
- [ ] Tool/access issue

**Root cause**: [What's actually causing this]

### Attempted Resolutions:
- [What you tried] - [Result]
- [What you tried] - [Result]

### Recommended Resolution Path:
**Option 1** (Preferred):
- Action: [What to do]
- Owner: [Who]
- Timeline: [How long]
- Confidence: [High/Medium/Low]

**Option 2** (Fallback):
- Action: [Alternative approach]
- Owner: [Who]
- Timeline: [How long]

### Escalation Decision:
**Escalate**: [Yes/No]

**If YES**:
- Escalate to: [Person/team]
- Reason: [Why escalation needed]
- Ask: [Specific request]
- Context to provide: [Background they need]

**If NO**:
- Self-resolve by: [Action plan]
- Check-in: [When to reassess]

### Temporary Workaround:
While blocked, can you:
- [Alternative task to make progress]
- [Parallel work that's not blocked]

### Communication Plan:
- [ ] Notify stakeholders: [Who] - [Message]
- [ ] Update task status
- [ ] Add to blocker log
- [ ] Standup mention: [Y/N]

### Follow-up:
- Next check: [Date/time]
- Expected resolution: [Date]
- If not resolved by [date]: [Escalation plan]
```

### Prompt 5: Sprint/Week Planning
```
ROLE: Sprint Planning Facilitator
CONTEXT: Planning next sprint/week of work

INPUT REQUIRED:
- Sprint duration: [1 week/2 weeks]
- Available capacity: [Hours available]
- Backlog priorities: [FROM_PLANNING_AGENT]
- Team velocity: [Historical average]
- Strategic goals: [FROM_STRATEGY_AGENT]
- Carry-over work: [INCOMPLETE_ITEMS]

TASK:
1. Calculate realistic capacity
2. Pull appropriate backlog items
3. Balance strategic vs tactical work
4. Identify dependencies and risks
5. Create sprint goal

OUTPUT FORMAT:
## Sprint/Week Plan - [DATE_RANGE]

### Sprint Goal:
[One clear sentence: What will we achieve this sprint?]

### Capacity Planning:
**Total Hours Available**: [X hours]
**Meetings/Admin**: [Y hours] (leave 20-25%)
**Net Development Time**: [Z hours]

**Team Velocity**: [Average points/tasks per sprint]
**This Sprint Commitment**: [Points/tasks] - [Conservative/On par/Aggressive]

### Strategic Alignment:
- Strategic work: [X%]
- Tactical improvements: [Y%]
- Tech debt/bugs: [Z%]

### Committed Work:

#### Priority 1: Must Ship 🎯
1. **[Task/Story]**
   - Points/Estimate: [X]
   - Owner: [You/Team]
   - Links to: [OKR/Goal]
   - Dependencies: [None/List]
   - Success criteria: [How we know it's done]

2. **[Task/Story]**
   - Points/Estimate: [X]
   - Owner: [You/Team]
   - Links to: [OKR/Goal]
   - Dependencies: [None/List]
   - Success criteria: [How we know it's done]

#### Priority 2: Should Ship 📋
[Items we expect to complete but not critical]

#### Priority 3: Nice to Have 💡
[Stretch goals if we're ahead]

### Dependencies & Risks:
**External Dependencies**:
- [Task] depends on [Team/Person] → [Status]

**Risks**:
- ⚠️ [Risk] - Mitigation: [Plan]

### Daily Breakdown (Recommended):
**Monday**: [Focus area]
**Tuesday**: [Focus area]
**Wednesday**: [Focus area]
**Thursday**: [Focus area]
**Friday**: [Wrap-up, testing, prep next week]

### Key Milestones:
- [Date]: [Milestone]
- [Date]: [Milestone]

### Definition of Done:
- [ ] Code complete
- [ ] Tests written
- [ ] Reviewed
- [ ] Documented
- [ ] Deployed to staging
- [ ] Stakeholder demo

### Communication Plan:
- **Daily standup**: [Time] - 15 min
- **Mid-sprint check**: [Day]
- **Demo/Review**: [Day/time]
- **Retrospective**: [Day/time]

### Success Metrics:
This sprint is successful if:
- ✅ [Specific outcome]
- ✅ [Specific outcome]
- ✅ [Velocity target: X% completion]
```

---

## Workflows

### Morning Workflow: Day Startup
```
TRIGGER: Every weekday at 7:30 AM

STEPS:
1. Pull today's calendar events
2. Review open tasks and priorities
3. Check for new urgent items
4. Get strategic priorities from Strategy Agent
5. Run "Daily Plan Generator"
6. Time-block calendar
7. Send plan to task system and/or email

ESTIMATED TIME: 10 minutes
OUTPUT: Ready-to-execute daily plan
```

### Midday Workflow: Progress Check
```
TRIGGER: Every weekday at 12:30 PM

STEPS:
1. Review morning plan
2. Check completed vs. pending
3. Identify any blockers
4. Run "Progress Check & Course Correction"
5. Adjust afternoon plan if needed
6. Alert on any critical issues

ESTIMATED TIME: 5 minutes
OUTPUT: Afternoon execution plan
```

### Evening Workflow: Day Close
```
TRIGGER: Every weekday at 5:30 PM

STEPS:
1. Review full day's activities
2. Mark tasks complete/incomplete
3. Capture blockers
4. Run "Daily Summary & Tomorrow Prep"
5. Update task system
6. Generate tomorrow's draft plan
7. Send summary to personal log

ESTIMATED TIME: 15 minutes
OUTPUT: Daily summary + Tomorrow preview
```

### Weekly Workflow: Sprint Planning
```
TRIGGER: Every Friday at 4:00 PM (or sprint start)

STEPS:
1. Review past sprint/week completion
2. Calculate velocity
3. Pull backlog from Planning Agent
4. Run "Sprint/Week Planning"
5. Commit to work items
6. Share plan with team
7. Setup tracking dashboard

ESTIMATED TIME: 1 hour
OUTPUT: Next sprint/week plan
```

---

## Decision Framework

### When to Escalate/Alert
```yaml
alert_conditions:
  critical:
    - Deadline at risk for committed deliverable
    - Blocker >24 hours unresolved affecting critical path
    - Completion rate <50% at mid-sprint
    - Resource unavailable for critical task

  high_priority:
    - Task taking 2x estimated time
    - Three or more blockers in one day
    - Competing urgent requests
    - Scope creep on committed work

  medium_priority:
    - Daily plan completion <70%
    - Meeting overload (>50% of day)
    - Lack of focus time for priorities
```

---

## Integration Checklist

### Required Connections
- [ ] Task management system (Jira/Asana/Linear)
- [ ] Calendar (Google/Outlook)
- [ ] Communication tool (Slack/Teams)
- [ ] Time tracking (Toggl/Harvest) - optional
- [ ] Project management (Notion/Confluence)

### Data Requirements
- [ ] All tasks have estimates
- [ ] Priorities clearly marked
- [ ] Deadlines set
- [ ] Task dependencies mapped
- [ ] Team velocity baseline (if applicable)

---

## Success Metrics

### Agent Performance KPIs
```yaml
effectiveness:
  - daily_plan_completion: "> 75%"
  - priority_task_completion: "> 90%"
  - blocker_resolution_time: "< 48 hours"

efficiency:
  - planning_time: "< 15 min/day"
  - focus_time_preserved: "> 3 hours/day"

predictability:
  - sprint_commitment_accuracy: "> 85%"
  - estimate_accuracy: "Within 20% variance"
```

---

## Example Usage

### Sample Input (Morning)
```
Calendar Today:
- 9:30-10:00: Standup
- 11:00-12:00: Design review
- 2:00-3:00: Stakeholder sync

Open Tasks:
- Finish PRD for Feature X (4h) - Due Friday
- Review design mocks (1h) - Due today
- Respond to customer feedback (30m)
- Update roadmap (1h) - Due next week
- 3 bug reports to triage (1h)

Strategic Priority: Feature X (supports Q1 OKR on activation)
```

### Sample Output
```
## Daily Execution Plan - 2026-01-01

### Top 3 Priorities:
1. **Review design mocks** - Unblocks designer - 1h - DEADLINE TODAY
2. **Finish PRD for Feature X** - Critical for Q1 OKR - 4h - Due Friday
3. **Customer feedback responses** - Maintain relationships - 30m

### Time-Blocked Schedule:
8:00-9:30 AM: [FOCUS] Design review prep + mock review
9:30-10:00 AM: Standup
10:00-11:00 AM: [FOCUS] Feature X PRD (part 1)
11:00-12:00 PM: Design review meeting
12:00-1:00 PM: Lunch + admin
1:00-2:00 PM: [FOCUS] Feature X PRD (part 2)
2:00-3:00 PM: Stakeholder sync
3:00-5:00 PM: [FOCUS] Feature X PRD (complete)
5:00-5:30 PM: Customer responses + wrap-up

### Secondary (if time): Bug triage, roadmap update

### Success Criteria:
✅ Design mocks reviewed and feedback given
✅ PRD 80%+ complete
✅ All customer responses sent
```

---

## Notes & Tips

1. **Be realistic**: Better to under-promise and over-deliver
2. **Protect focus time**: Block calendar for deep work
3. **Track blockers immediately**: Don't let them fester
4. **Celebrate wins**: Note progress daily for motivation
5. **Adjust, don't abandon**: If plans change, revise rather than give up
