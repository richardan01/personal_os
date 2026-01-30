# Personal OS Reference Library

> Quick reference guide for using skills, agents, and commands effectively.

---

## Skills vs Agents: When to Use Which

### TL;DR

| You need... | Use | Syntax |
|-------------|-----|--------|
| A specific output | **Skill (Command)** | `/daily-plan` |
| Broad thinking/collaboration | **Agent** | `@strategy-agent` |

---

## Skills (Commands)

**What they are:** Focused, single-purpose tasks with defined inputs and outputs.

**When to use:**
- You know exactly what you want
- Need a specific deliverable
- Want consistent, repeatable output

**Syntax:** `/command-name`

### Available Skills

| Command | Purpose | Output |
|---------|---------|--------|
| `/daily-plan` | Generate prioritized daily plan | Time-blocked schedule with top 3 priorities |
| `/progress-check` | Midday assessment | Progress update with adjustments |
| `/daily-summary` | End-of-day wrap-up | Summary with tomorrow prep |
| `/sprint-plan` | Sprint planning | Sprint goals, capacity, commitments |
| `/strategy-check` | OKR alignment check | Alignment assessment with recommendations |
| `/discovery` | Research synthesis | Themes, insights, recommendations |
| `/stakeholder-update` | Status report | Tailored update for specific audience |
| `/update-context` | Edit your context | Interactive context editor |
| `/personal-os` | Command hub | Show all available commands |

---

## Agents

**What they are:** Personas with expertise, judgment, and broader capabilities.

**When to use:**
- Task is ambiguous or exploratory
- Need multi-step collaboration
- Want strategic thinking and advice
- Working through complex decisions

**Syntax:** `@agent-name`

### Available Agents

| Agent | Expertise | Model | Best For |
|-------|-----------|-------|----------|
| `@execution-agent` | Daily productivity | Sonnet | Task management, daily rhythm |
| `@planning-agent` | Agile, prioritization | Sonnet | Sprint planning, backlog management |
| `@strategy-agent` | OKRs, strategic planning | Opus | Vision alignment, quarterly planning |
| `@discovery-agent` | User research | Sonnet | Interview synthesis, feedback analysis |
| `@stakeholder-agent` | Communications | Sonnet | Status reports, meeting prep |
| `@analytics-agent` | Metrics, experiments | Sonnet | Data analysis, A/B tests |
| `@documentation-agent` | Knowledge management | Sonnet | PRDs, decision logs |
| `@learning-agent` | Continuous improvement | Haiku | Retrospectives, skill development |
| `@product-manager` | Full PM capabilities | Opus | Complex PM tasks, strategic decisions |

---

## Decision Matrix

| Scenario | Use |
|----------|-----|
| "I need today's plan" | `/daily-plan` |
| "Help me think through my priorities" | `@strategy-agent` |
| "Create a sprint plan" | `/sprint-plan` |
| "Should we prioritize X or Y?" | `@planning-agent` |
| "Write a stakeholder update" | `/stakeholder-update` |
| "How should I communicate this bad news?" | `@stakeholder-agent` |
| "Synthesize these interview notes" | `/discovery` |
| "What patterns do you see in customer feedback?" | `@discovery-agent` |
| "I need a PRD for feature X" | `@product-manager` |
| "Help me plan my quarter" | `@strategy-agent` |

---

## How They Work Together

```
User Request
     │
     ▼
┌─────────────────────────────────────────┐
│  COMMANDS (Skills)                      │
│  /daily-plan, /sprint-plan, etc.        │
│  → Specific output, defined format      │
└────────────────┬────────────────────────┘
                 │ route to
                 ▼
┌─────────────────────────────────────────┐
│  AGENTS                                 │
│  @execution-agent, @strategy-agent      │
│  → Personas that execute skills         │
└────────────────┬────────────────────────┘
                 │ reference
                 ▼
┌─────────────────────────────────────────┐
│  SHARED CONTEXT                         │
│  agents/_shared/context.md              │
│  → Your OKRs, priorities, stakeholders  │
└─────────────────────────────────────────┘
```

---

## Agent-Skill Mapping

### @execution-agent
- `/daily-plan` - Morning planning
- `/progress-check` - Midday assessment
- `/daily-summary` - Evening wrap-up

### @planning-agent
- `/sprint-plan` - Sprint planning and capacity

### @strategy-agent
- `/strategy-check` - OKR alignment assessment

### @discovery-agent
- `/discovery` - User research synthesis

### @stakeholder-agent
- `/stakeholder-update` - Status reports for any audience

### @analytics-agent
- *(Skills coming soon)*

### @documentation-agent
- *(Skills coming soon)*

### @learning-agent
- *(Skills coming soon)*

### @product-manager
- Full PM capabilities (no specific skills - acts as comprehensive PM advisor)

---

## Quick Examples

### Morning Routine
```
/daily-plan
```
Get your prioritized daily schedule.

### Need Strategic Advice
```
@strategy-agent

I'm struggling to balance feature development with tech debt.
Our Q1 OKR is focused on user activation but engineering wants
to refactor the auth system. How should I think about this?
```

### Prepare for a Difficult Meeting
```
@stakeholder-agent

I need to tell leadership that Feature X is delayed by 3 weeks.
Help me prepare for this conversation.
```

### Quick Status Update
```
/stakeholder-update

Audience: Engineering team
Topics: Sprint progress, blockers, next week focus
```

---

## Tips

1. **Start with skills** for known tasks - they're faster and more consistent
2. **Escalate to agents** when you need thinking, not just output
3. **Use @product-manager** as the "Swiss Army knife" for complex PM tasks
4. **All agents share your context** - no need to repeat your OKRs or priorities
5. **Skills are reusable** - any agent can execute any skill

---

## Updating Your Context

Your personal context (OKRs, priorities, stakeholders) is stored in:
```
.claude/agents/_shared/context.md
```

Update it with `/update-context` or edit the file directly.

All agents and skills reference this file, so changes propagate everywhere.
