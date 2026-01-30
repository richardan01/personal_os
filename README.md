# Personal OS for Product Management

> AI-powered productivity system with specialized agents that help you plan, execute, and communicate more effectively.

---

## Quick Start

Run `/personal-os` to see all available commands, or use these directly:

| Time | Command | What it does |
|------|---------|--------------|
| Morning | `/daily-plan` | Plan your day |
| Midday | `/progress-check` | Assess and adjust |
| Evening | `/daily-summary` | Wrap up and prep tomorrow |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        COMMANDS                              │
│  Thin routers (~15 lines) that connect users to the system  │
│                                                              │
│  /daily-plan  /progress-check  /discovery  /strategy-check  │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                         AGENTS                               │
│     Personas with interaction styles and skill routing       │
│                                                              │
│  @execution-agent   @strategy-agent    @discovery-agent     │
│  @planning-agent    @stakeholder-agent @analytics-agent     │
└─────────────────────────┬───────────────────────────────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
┌───────────────┐ ┌─────────────┐ ┌─────────────────┐
│    SKILLS     │ │   SHARED    │ │     OUTPUT      │
│  Pure "how    │ │   CONTEXT   │ │    FORMATS      │
│  to" guides   │ │  OKRs, user │ │   Templates     │
│               │ │  priorities │ │                 │
└───────────────┘ └─────────────┘ └─────────────────┘
```

### Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Single source of truth** | All user context in `agents/_shared/context.md` |
| **Skills are stateless** | No persona, just instructions - any agent can use |
| **Agents orchestrate** | Know which skills to use, when to hand off |
| **Commands route** | Minimal logic, connect user to agent+skill |
| **Loose coupling** | Skills reusable across agents |

---

## Available Commands

### Execution (Daily Operations)
| Command | Description | Agent |
|---------|-------------|-------|
| `/daily-plan` | Morning planning | @execution-agent |
| `/progress-check` | Midday assessment | @execution-agent |
| `/daily-summary` | Evening wrap-up | @execution-agent |

### Planning
| Command | Description | Agent |
|---------|-------------|-------|
| `/sprint-plan` | Sprint planning | @planning-agent |
| `/strategy-check` | OKR alignment | @strategy-agent |

### Research
| Command | Description | Agent |
|---------|-------------|-------|
| `/discovery` | User research synthesis | @discovery-agent |

### Communication
| Command | Description | Agent |
|---------|-------------|-------|
| `/stakeholder-update` | Status reports | @stakeholder-agent |

### Configuration
| Command | Description | Agent |
|---------|-------------|-------|
| `/update-context` | Update OKRs, priorities, and user profile | Interactive |

---

## Agents

Each agent has a specific persona and orchestrates related skills:

| Agent | Purpose | Model |
|-------|---------|-------|
| `@execution-agent` | Daily operations, productivity | Sonnet |
| `@strategy-agent` | OKRs, strategic alignment | Opus |
| `@discovery-agent` | User research, feedback | Sonnet |
| `@planning-agent` | Sprints, prioritization | Sonnet |
| `@stakeholder-agent` | Communications, updates | Sonnet |
| `@analytics-agent` | Metrics, experiments | Sonnet |
| `@documentation-agent` | PRDs, knowledge base | Sonnet |
| `@learning-agent` | Growth, retrospectives | Haiku |
| `@product-manager` | Full PM capabilities | Opus |

---

## File Structure

```
.claude/
├── commands/                    # Thin routers (~15 lines each)
│   ├── personal-os.md          # Main hub
│   ├── daily-plan.md           # → @execution-agent
│   ├── progress-check.md       # → @execution-agent
│   ├── daily-summary.md        # → @execution-agent
│   ├── sprint-plan.md          # → @planning-agent
│   ├── strategy-check.md       # → @strategy-agent
│   ├── discovery.md            # → @discovery-agent
│   └── stakeholder-update.md   # → @stakeholder-agent
│
├── agents/                      # Personas + skill orchestration
│   ├── _shared/
│   │   └── context.md          # User profile, OKRs, priorities
│   ├── execution-agent.md
│   ├── strategy-agent.md
│   ├── discovery-agent.md
│   ├── planning-agent.md
│   ├── stakeholder-agent.md
│   ├── analytics-agent.md
│   ├── documentation-agent.md
│   ├── learning-agent.md
│   └── product-manager.md      # Swiss Army knife fallback
│
└── skills/                      # Pure instructions (persona-free)
    ├── _shared/
    │   └── output-formats.md   # Shared templates
    ├── execution/
    │   ├── daily-plan.md
    │   ├── progress-check.md
    │   └── daily-summary.md
    ├── planning/
    │   ├── sprint-plan.md
    │   └── strategy-check.md
    ├── research/
    │   └── discovery.md
    └── communication/
        └── stakeholder-update.md
```

---

## Customization

### Update Your Context

Edit `.claude/agents/_shared/context.md` to customize:
- Your name and role
- Current OKRs
- Strategic priorities
- Working style preferences
- Key stakeholders

This file is the single source of truth - all agents reference it.

### Add New Skills

1. Create a new file in the appropriate `skills/` subdirectory
2. Follow the skill template (Purpose, Inputs, Instructions, Output Format, Quality Checks)
3. Add it to the relevant agent's "Skills I Orchestrate" table
4. Optionally create a command that routes to it

---

## Python Automation (Optional)

For automated background workflows:

```
automation/
├── main.py
├── config.py
└── requirements.txt
```

Setup:
1. `cd automation`
2. `pip install -r requirements.txt`
3. Configure API keys in `.env`
4. `python main.py`

---

## Reference Library

See `.claude/REFERENCE.md` for:
- When to use skills vs agents
- Complete command and agent listing
- Decision matrix for common scenarios
- Quick examples

---

**Built for Product Managers who want to focus on building great products, not managing tasks.**
