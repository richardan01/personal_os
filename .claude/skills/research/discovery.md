# Discovery & Research Synthesis

## Purpose

Synthesize user research, customer feedback, and discovery data into actionable insights that drive product decisions.

## Inputs Required

- **Research data**: Interview notes, feedback, survey results
- **Context**: User segments, personas, current focus areas
- **Reference**: Priorities from `@context:agents/_shared/context`

## Instructions

1. **Gather the Data**
   - Ask user to share their research/feedback data
   - Ask about context: what prompted this research?
   - Ask about user segments involved

2. **Extract Themes**
   - Identify recurring patterns across data points
   - Note frequency of each theme
   - Preserve powerful direct quotes

3. **Analyze Pain Points**
   - Categorize by type (bug, UX, feature gap, etc.)
   - Assess severity and frequency
   - Map to user segments/personas

4. **Uncover Real Needs**
   - Look beyond stated requests to underlying needs
   - Apply Jobs-to-be-Done framework
   - Identify the "job" users are trying to accomplish

5. **Generate Recommendations**
   - Quick wins: actionable now
   - Investigate: needs more research
   - Strategic: bigger considerations

## Jobs-to-be-Done Framework

When analyzing requests, identify:
- **Job**: What is the user trying to accomplish?
- **Current solution**: How do they do it today?
- **Desired outcome**: What would success look like?
- **Barriers**: What's preventing success?

## Output Format

Reference: `@template:skills/_shared/output-formats#discovery-insights-template`

```markdown
## Discovery Insights - [Topic/Date]

### Summary
[2-3 sentence overview of key findings]

### Key Themes
1. **[Theme 1]**: [Description]
   - Evidence: [Quote or data point]
   - Frequency: [How often mentioned]
   - Affected Personas: [Who]

2. **[Theme 2]**: [Description]
   - Evidence: [Quote or data point]
   - Frequency: [How often mentioned]
   - Affected Personas: [Who]

### Pain Points Identified
| Pain Point | Severity | Frequency | Segment |
|------------|----------|-----------|---------|
| [Issue] | H/M/L | Often/Sometimes/Rare | [Who] |

### Feature Requests (Mapped to Needs)
| Request | Underlying Need | JTBD | Priority |
|---------|-----------------|------|----------|
| [What they asked for] | [What they actually need] | [Job] | H/M/L |

### Notable Quotes
> "[Direct quote]" - [User type/context]
> "[Direct quote]" - [User type/context]

### Recommendations
1. **Quick Win**: [Something actionable now]
   - Effort: Low | Impact: [Assessment]
2. **Investigate Further**: [Something needing more research]
   - Next step: [Specific action]
3. **Strategic Consideration**: [Bigger picture item]
   - Impact on: [OKR/Priority]

### Open Questions
- [What we still need to learn]
- [Hypothesis to validate]
```

## Quality Checks

- [ ] Looked for patterns, not just individual data points
- [ ] Distinguished stated wants from underlying needs
- [ ] Preserved user voice with direct quotes
- [ ] Recommendations are actionable with clear next steps
- [ ] Connected findings to strategic priorities
