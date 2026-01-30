# /update-context

> Interactive editor for your Personal OS context - update OKRs, priorities, and more without editing files manually.

## How to Use

When invoked, guide the user through updating their context interactively.

## Context File Location

All context is stored in: `.claude/agents/_shared/context.md`

## Available Sections

| Section | What It Contains |
|---------|------------------|
| **OKRs** | Objectives, Key Results, Targets |
| **Strategic Priorities** | Top 3 ranked priorities |
| **Sprint Focus** | Primary, secondary, stretch goals |
| **User Profile** | Name, role, company |
| **Stakeholders** | Key people and communication preferences |
| **Roadmap** | Initiatives, timelines, status |

## Workflow

### Step 1: Ask What to Update

Present this menu:

```
What would you like to update?

1. OKRs - Your objectives and key results
2. Strategic Priorities - Your top 3 focus areas
3. Sprint Focus - Current sprint goals
4. User Profile - Name, role, company
5. Stakeholders - Key people you work with
6. Roadmap - Initiatives and timelines
7. Full Review - Walk through everything
```

### Step 2: Show Current Values

After selection, read the current context file and show the relevant section.

### Step 3: Gather Updates

Based on selection, ask targeted questions:

**For OKRs:**
- What would you like to do? (Add / Edit / Remove)
- What's the objective?
- What's the key result?
- What's the target?

**For Strategic Priorities:**
- What are your top 3 priorities?
- Brief description for each?

**For Sprint Focus:**
- What's your primary goal this sprint?
- Secondary goal?
- Stretch goal?

**For User Profile:**
- What's your name?
- What's your role?
- What company?

**For Stakeholders:**
- Who are the key stakeholders?
- What are their roles?
- Communication preferences?

**For Roadmap:**
- What initiatives are planned?
- Which OKR does each support?
- Timeline and status?

### Step 4: Confirm Changes

Before saving, show the user what will be updated:

```
Here's what I'll update:

[Show the new content]

Does this look correct?
```

### Step 5: Save Changes

Use the Edit tool to update `.claude/agents/_shared/context.md` with the new values.

### Step 6: Confirm Success

```
Updated! Your context has been saved.

Changes made:
- [List what changed]

All agents will now use your updated context.
```

## Output Format

When showing current values, use clear formatting:

```markdown
## Current OKRs

| # | Objective | Key Result | Target |
|---|-----------|------------|--------|
| 1 | [Objective] | [KR] | [Target] |
| 2 | [Objective] | [KR] | [Target] |

What would you like to do?
- **Add** - Add a new OKR
- **Edit** - Modify an existing OKR (specify number)
- **Remove** - Delete an OKR (specify number)
- **Done** - Finish and save
```

## Important Notes

- Always read the current context file before making changes
- Preserve sections the user isn't updating
- Use the Edit tool to make surgical changes, not Write to overwrite everything
- Confirm changes before saving
- Be conversational and helpful throughout the process
