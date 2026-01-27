# Strategy Alignment Check

## Purpose

Assess how well current activities align with strategic goals and OKRs, identify gaps, and recommend course corrections.

## Inputs Required

- **Current activities**: What you're working on now
- **Recent accomplishments**: What's been completed recently
- **Context**: OKRs and priorities from `@context:agents/_shared/context`

## Instructions

1. **Gather Information**
   - Ask about current focus areas and activities
   - Ask about recent accomplishments
   - Ask about planned work for coming week/month

2. **Map to OKRs**
   - For each activity, identify which OKR/priority it supports
   - Calculate alignment score (1-10)
   - Identify activities with weak or no alignment

3. **Assess Progress**
   - Review progress against each OKR
   - Determine status: On Track, At Risk, Behind
   - Identify blockers to OKR progress

4. **Identify Opportunities**
   - Find high-leverage activities being missed
   - Suggest focus shifts if needed
   - Recommend strategic priorities for this week/month

5. **Generate Questions**
   - Surface strategic questions that need answering
   - Challenge assumptions if appropriate

## Output Format

Reference: `@template:skills/_shared/output-formats#strategy-check-template`

```markdown
## Strategy Alignment Check - [Date]

### OKR Progress Snapshot
| Objective | Key Result | Progress | Status |
|-----------|------------|----------|--------|
| Improve activation | +25% activation rate | [X%] | [On Track/At Risk/Behind] |
| Launch feature X | Feature shipped | [X%] | [Status] |
| Reduce churn | -10% churn rate | [X%] | [Status] |

### Alignment Score: [X/10]
[Assessment of how well current activities align with strategy]

### Current Work Alignment

**Aligned Activities:**
- [Activity] -> Supports: [OKR/Priority] - Alignment: Strong
- [Activity] -> Supports: [OKR/Priority] - Alignment: Strong

**Potentially Misaligned:**
- [Activity] - Question: [Why this might not serve strategic goals]
- [Activity] - Question: [Concern about priority]

### Strategic Opportunities
Based on your priorities, consider:
1. [Opportunity 1] - Impact on: [OKR/Priority]
2. [Opportunity 2] - Impact on: [OKR/Priority]

### Recommended Focus Areas

**This Week:**
- [Focus 1] - Moves: [OKR] forward
- [Focus 2] - Moves: [OKR] forward

**This Month:**
- [Larger initiative] - Strategic impact: [Description]

### Risks to Strategy
- [Risk 1] - Mitigation: [Suggestion]
- [Risk 2] - Mitigation: [Suggestion]

### Questions to Consider
- [Strategic question that needs answering]
- [Assumption that should be validated]
```

## Quality Checks

- [ ] Every activity is mapped to an OKR/priority (or flagged as misaligned)
- [ ] Recommendations are specific and actionable
- [ ] Assessment is constructive, not critical
- [ ] Focus on highest-leverage opportunities
- [ ] Strategy connected to daily execution
