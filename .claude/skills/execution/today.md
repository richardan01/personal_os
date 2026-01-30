# Today Overview

## Purpose

Provide an instant, question-free overview of today's schedule and priorities.

## Instructions

1. **Get Calendar Events**
   - Fetch today's events from Google Calendar
   - Display time, title, and location/link

2. **Show Priorities**
   - Pull current sprint focus from context
   - List top 3 strategic priorities

3. **Output Format**
   - Keep it concise and scannable
   - No questions, no planning - just information

## Output Format

```markdown
## Today - [Day, Date]

### Calendar
| Time | Event | Location |
|------|-------|----------|
| [Time] | [Event] | [Link/Location] |

### Current Focus
- Primary: [From context]
- Secondary: [From context]

### Quick Links
- [Any relevant meeting links]
```

## Quality Checks

- [ ] Shows all calendar events for today
- [ ] Includes times in readable format
- [ ] Displays current priorities from context
- [ ] No questions asked - immediate output
