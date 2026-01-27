# Stakeholder Update Generation

## Purpose

Generate clear, audience-appropriate stakeholder communications that inform, align, and drive action.

## Inputs Required

- **Audience**: Who is this for? (executives, team, partners)
- **Time period**: What period to cover
- **Content**: Progress, metrics, highlights, risks
- **Context**: Stakeholder preferences from `@context:agents/_shared/context`

## Instructions

1. **Identify Audience**
   - Ask who the update is for
   - Determine appropriate detail level
   - Understand their key concerns/interests

2. **Gather Content**
   - Ask about time period to cover
   - Collect progress, wins, and metrics
   - Identify risks and blockers
   - Note any decisions needed

3. **Adapt Format**
   - Executives: TL;DR first, metrics, strategic view
   - Team: Sprint progress, detailed updates, recognition
   - Partners: Collaborative view, dependencies, timelines

4. **Structure the Update**
   - Lead with most important information
   - Be honest about challenges (with mitigations)
   - Make asks specific and actionable
   - Include clear next steps

## Output Formats

### For Executives

```markdown
## Executive Update - [Date]

### TL;DR
[2-3 sentences max - what they need to know]

### Key Metrics
| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| [KPI 1] | [Value] | [Goal] | [Up/Down/Flat] |

### Highlights
- [Win 1] - [Impact]
- [Win 2] - [Impact]

### Risks & Blockers
| Issue | Impact | Mitigation | Need from Leadership |
|-------|--------|------------|---------------------|
| [Risk] | H/M/L | [Plan] | [Decision/Resource/None] |

### Decisions Needed
- [ ] [Decision 1] - Deadline: [Date]

### Next Week Focus
[One paragraph on priorities]
```

### For Team

```markdown
## Team Update - [Date]

### Sprint Progress
- **Completed**: [X/Y stories]
- **In Progress**: [X stories]
- **Blocked**: [X stories]

### What Shipped
- [Feature/Fix 1] - [Impact]
- [Feature/Fix 2] - [Impact]

### Coming Up
- [Next priority 1]
- [Next priority 2]

### Blockers & Needs
- [Blocker] - Need: [What would help]

### Shoutouts
- [Recognition for team member]
```

### Weekly Status Report

```markdown
## Weekly Status Report - Week of [Date]

### Summary
[Executive summary paragraph]

### Progress vs Plan
| Planned | Status | Notes |
|---------|--------|-------|
| [Item] | [Complete/In Progress/Blocked] | [Context] |

### Accomplishments
1. [Accomplishment with impact]
2. [Accomplishment with impact]

### Challenges
1. [Challenge] - Mitigation: [Plan]

### Next Week Plan
1. [Priority 1]
2. [Priority 2]

### Help Needed
- [Specific ask with owner]
```

## Quality Checks

- [ ] Detail level matches audience expectations
- [ ] Most important information comes first
- [ ] Challenges include mitigations (not just problems)
- [ ] Asks are specific with clear owners/deadlines
- [ ] Tone is appropriate for the audience
