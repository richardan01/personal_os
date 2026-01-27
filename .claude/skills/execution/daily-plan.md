# Daily Plan Generation

## Purpose

Generate a comprehensive daily execution plan that maximizes productivity and aligns with strategic priorities.

## Inputs Required

- **Today's date**: Current date and day of week
- **Calendar events**: Meetings and commitments
- **Open tasks**: Current task list and priorities
- **Context**: User profile, OKRs, and priorities from `@context:agents/_shared/context`

## Instructions

1. **Gather Information**
   - If not provided, ask about today's meetings and commitments
   - Ask about most important tasks and deadlines
   - Ask about any blockers or constraints

2. **Analyze the Day**
   - Calculate available focus time (total hours minus meetings)
   - Assess energy demands based on meeting load
   - Identify best time blocks for deep work

3. **Create Priorities**
   - Select top 3 priorities that move strategic goals forward
   - Ensure priorities are achievable within available time
   - Connect each to OKRs or strategic priorities

4. **Build the Schedule**
   - Time-block the day hour by hour
   - Place deep work in morning when possible
   - Add buffer time between meetings
   - Include breaks for sustainability

5. **Define Success**
   - Write 3 specific, measurable success criteria
   - Make them achievable but meaningful

## Output Format

Reference: `@template:skills/_shared/output-formats#daily-plan-template`

```markdown
## Daily Execution Plan - [Today's Date]

### Day Overview
- **Focus Time**: [X hours]
- **Meetings**: [Count] ([Y hours])
- **Energy Forecast**: [High/Medium/Demanding]

### Top 3 Priorities
1. **[Task]** - [Why it matters] - [Time estimate]
   - Links to: [Strategic goal/OKR]
2. **[Task]** - [Why it matters] - [Time estimate]
   - Links to: [Strategic goal/OKR]
3. **[Task]** - [Why it matters] - [Time estimate]
   - Links to: [Strategic goal/OKR]

### Time-Blocked Schedule
| Time | Activity | Type |
|------|----------|------|
| 8:00-9:00 | [Task] | Focus |
| 9:00-9:30 | [Task] | Admin |
| ... | ... | ... |

### Meeting Preparation
For each meeting:
- **[Meeting name]**: [Prep needed] - Objective: [Goal]

### Success Criteria
Today is successful if:
1. [Specific, measurable outcome]
2. [Specific, measurable outcome]
3. [Specific, measurable outcome]

### Potential Risks
- [Any scheduling conflicts or overcommitment flags]
```

## Quality Checks

- [ ] Priorities are realistic for available time
- [ ] Deep work scheduled during high-energy periods
- [ ] Buffer time included (not over-scheduled)
- [ ] All priorities connect to strategic goals
- [ ] Success criteria are specific and measurable
