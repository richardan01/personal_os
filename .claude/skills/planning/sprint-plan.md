# Sprint Planning

## Purpose

Plan and organize sprints for maximum delivery and impact, with realistic commitments and clear dependencies.

## Inputs Required

- **Team capacity**: Team size, sprint length, available points/hours
- **Backlog items**: Stories/tasks to consider for the sprint
- **Dependencies**: Known blockers and cross-team dependencies
- **Context**: OKRs and priorities from `@context:agents/_shared/context`

## Instructions

1. **Gather Information**
   - Ask about team size and sprint length
   - Ask about velocity/capacity (points or hours)
   - Gather backlog items to consider
   - Identify any known dependencies or constraints

2. **Calculate Capacity**
   - Determine gross capacity
   - Apply 20% buffer for unknowns
   - Calculate net committable capacity

3. **Prioritize Items**
   - Apply appropriate framework (RICE, MoSCoW, etc.)
   - Categorize into P0 (Must), P1 (Should), P2 (Stretch)
   - Ensure total doesn't exceed capacity

4. **Map Dependencies**
   - Identify cross-team dependencies
   - Find technical dependencies
   - Flag blocking items
   - Determine critical path

5. **Define Success**
   - Write one clear, measurable sprint goal
   - Define key milestones
   - Set success criteria

## Prioritization Frameworks

**RICE Score** = (Reach x Impact x Confidence) / Effort
- Reach: Users affected (1-10)
- Impact: How much it matters (0.25, 0.5, 1, 2, 3)
- Confidence: How sure (0.5, 0.8, 1)
- Effort: Person-weeks

**MoSCoW**:
- Must have: Critical for sprint goal
- Should have: Important but not critical
- Could have: Nice to have
- Won't have: Out of scope

## Output Format

Reference: `@template:skills/_shared/output-formats#sprint-plan-template`

```markdown
## Sprint Plan - Sprint [X] ([Date Range])

### Sprint Goal
[One clear, measurable goal for this sprint]

### Capacity
- Team Size: [X developers]
- Sprint Length: [X days/weeks]
- Gross Capacity: [X points/hours]
- Buffer (20%): [X]
- **Net Committable**: [X]

### Committed Items

#### P0 - Must Complete
| Story | Points | Owner | Dependencies |
|-------|--------|-------|--------------|
| [Story] | [X] | [Name] | [None/Blocked by] |

#### P1 - Should Complete
| Story | Points | Owner | Dependencies |
|-------|--------|-------|--------------|

#### P2 - Stretch Goals
| Story | Points | Owner | Dependencies |
|-------|--------|-------|--------------|

### Total Committed: [X points] / [Net Capacity]

### Dependencies & Risks
| Dependency | Owner | Status | Risk Level |
|------------|-------|--------|------------|
| [Item] | [Who] | [Status] | [H/M/L] |

### Key Milestones
- Day [X]: [Milestone]
- Day [Y]: [Milestone]
- Final Day: Sprint Review

### Definition of Done
- [ ] Code complete and reviewed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Product sign-off

### Success Criteria
By end of sprint:
1. [Measurable outcome]
2. [Measurable outcome]
```

## Quality Checks

- [ ] Total commitment does not exceed net capacity
- [ ] Sprint goal is clear and measurable
- [ ] Dependencies are mapped and owners assigned
- [ ] P0 items are truly critical
- [ ] 20% buffer is maintained
