# Daily Summary

## Purpose

Create an end-of-day summary that captures accomplishments, documents learnings, and sets up tomorrow for success.

## Inputs Required

- **Day's activities**: What was planned and what happened
- **Completed tasks**: What got done and outcomes
- **Incomplete tasks**: What rolled over and why
- **Context**: User profile from `@context:agents/_shared/context`

## Instructions

1. **Gather Information**
   - Ask about what was accomplished today
   - Ask about what didn't get done and why
   - Ask about any blockers encountered
   - Ask about wins and challenges

2. **Assess the Day**
   - Score achievement on 1-10 scale
   - Calculate completion rate
   - Identify patterns in what worked/didn't

3. **Document Outcomes**
   - List completed items with their impact
   - List rolled items with clear reasons
   - Capture blockers with resolution status

4. **Extract Learnings**
   - Identify insights about work patterns
   - Note what went well to repeat
   - Note what to improve

5. **Prepare Tomorrow**
   - Draft top 3 priorities based on rollovers and upcoming deadlines
   - End on a positive, forward-looking note

## Output Format

Reference: `@template:skills/_shared/output-formats#daily-summary-template`

```markdown
## Daily Summary - [Today's Date]

### Achievement Score: [X/10]
[Overall rating with brief explanation]

### Completed
- [Task 1] - Outcome: [Impact/result]
- [Task 2] - Outcome: [Impact/result]

**Completion Rate**: [X/Y tasks] = [Z%]

### Rolled to Tomorrow
- [Task 1] - Reason: [Why it wasn't completed]
- [Task 2] - Reason: [Why it wasn't completed]

### Blockers Encountered
| Blocker | Impact | Status | Next Action |
|---------|--------|--------|-------------|
| [Issue] | [H/M/L] | [Resolved/Open] | [What to do] |

### What Went Well
- [Win 1] - [Why it worked]
- [Win 2] - [Why it worked]

### What Could Be Better
- [Challenge 1] - Potential solution: [Idea]
- [Challenge 2] - Potential solution: [Idea]

### Key Learning
[Insight about work patterns, productivity, or process]

### Tomorrow's Priorities (Draft)
Based on rollovers and upcoming deadlines:
1. **[Priority 1]** - [Why it's important]
2. **[Priority 2]** - [Why it's important]
3. **[Priority 3]** - [Why it's important]

### Closing Thought
[Positive reflection and motivation for tomorrow]
```

## Quality Checks

- [ ] Assessment is honest but encouraging
- [ ] Learnings are specific and actionable
- [ ] Rolled items have clear reasons (not just "didn't get to it")
- [ ] Tomorrow's priorities are actionable
- [ ] Ends on a positive, forward-looking note
