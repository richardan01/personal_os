# Progress Check

## Purpose

Perform a mid-day assessment of progress against the morning plan and recommend adjustments for the remaining time.

## Inputs Required

- **Morning plan**: Reference to today's daily plan
- **Completed tasks**: What's been accomplished so far
- **Current status**: What's in progress or blocked
- **Context**: User profile from `@context:agents/_shared/context`

## Instructions

1. **Gather Status**
   - Ask what has been completed today
   - Ask about any blockers or unexpected issues
   - Ask about energy level and focus quality

2. **Assess Progress**
   - Calculate completion rate against morning plan
   - Score progress on 1-10 scale with explanation
   - Determine if ahead, on track, or behind

3. **Recommend Adjustments**
   - If behind: identify what to defer, timebox, or get help with
   - If on track: suggest stretch goals
   - If ahead: recommend strategic priorities to tackle

4. **Revise Afternoon Plan**
   - Create revised time blocks for remaining hours
   - Prioritize most impactful work
   - Include recovery time if needed

5. **Energy Management**
   - Provide tip for managing afternoon energy
   - Suggest appropriate work type for energy level

## Output Format

Reference: `@template:skills/_shared/output-formats#progress-check-template`

```markdown
## Progress Check - [Current Time]

### Progress Score: [X/10]
[Brief explanation of the rating]

### Completed Today
- [Task 1] - Impact: [High/Medium/Low]
- [Task 2] - Impact: [High/Medium/Low]

### Status Assessment
**Status**: [Ahead of schedule / On track / Behind / Significantly behind]

[Explanation of why this assessment]

### In Progress
- [Task currently being worked on] - [Status]

### Not Yet Started
- [Pending tasks from morning plan]

### Recommended Adjustments

**Actions to take:**
- Defer to tomorrow: [items if any]
- Timebox: [items with time limits]
- Get help with: [items needing support]
- Stretch goals: [if ahead of schedule]

### Afternoon Plan (Revised)
| Time | Priority | Notes |
|------|----------|-------|
| [Time] | [Task] | [Context] |

### Energy Check
[Quick tip for managing afternoon energy based on current state]
```

## Quality Checks

- [ ] Assessment is honest but supportive
- [ ] Adjustments are actionable and specific
- [ ] Revised plan is realistic for remaining time
- [ ] Focus is on what CAN be done, not what wasn't
- [ ] Ends with encouragement
