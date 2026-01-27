# /personal-os

> Personal OS Command Center - your AI-powered productivity hub.

## Quick Start

Based on time of day:
- **Morning**: `/daily-plan` - Plan your day
- **Midday**: `/progress-check` - Assess and adjust
- **Evening**: `/daily-summary` - Wrap up

## Available Commands

### Execution
| Command | Description |
|---------|-------------|
| `/daily-plan` | Generate morning daily plan |
| `/progress-check` | Mid-day progress assessment |
| `/daily-summary` | End-of-day summary |

### Planning
| Command | Description |
|---------|-------------|
| `/sprint-plan` | Sprint planning and prioritization |
| `/strategy-check` | OKR alignment check |

### Research
| Command | Description |
|---------|-------------|
| `/discovery` | User research synthesis |

### Communication
| Command | Description |
|---------|-------------|
| `/stakeholder-update` | Status reports for any audience |

## Agents

Invoke agents with `@agent-name`:

| Agent | Purpose |
|-------|---------|
| `@execution-agent` | Daily operations |
| `@strategy-agent` | Strategic planning |
| `@discovery-agent` | User research |
| `@planning-agent` | Sprint planning |
| `@stakeholder-agent` | Communications |
| `@analytics-agent` | Data & metrics |
| `@documentation-agent` | Knowledge management |
| `@learning-agent` | Continuous improvement |
| `@product-manager` | Full PM capabilities |

## Architecture

```
Commands → route to → Agents → execute → Skills
                         ↓
                   Shared Context
```

All agents reference shared context from `agents/_shared/context.md` for consistent user info, OKRs, and priorities.
