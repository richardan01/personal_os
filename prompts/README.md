# Personal OS Agents - Implementation Guide

## Overview

This directory contains detailed implementation templates for your Personal OS agents. Each agent is designed to handle specific aspects of product management work, with ready-to-use prompts, workflows, and integration guidelines.

---

## Agent Files

### 1. [Strategy Agent](./strategy-agent.md)
**Focus**: Strategic planning, OKR management, competitive analysis
- Daily strategy alignment checks
- OKR planning and tracking
- Roadmap strategic reviews
- Competitive intelligence synthesis

**Best for**: Ensuring your daily work ladders up to strategic goals

---

### 2. [Discovery Agent](./discovery-agent.md)
**Focus**: User research, feedback analysis, requirement gathering
- Interview synthesis
- Feature request analysis
- Feedback trend detection
- User persona creation

**Best for**: Turning raw user feedback into actionable product insights

---

### 3. [Execution Agent](./execution-agent.md)
**Focus**: Task management, delivery tracking, blocker resolution
- Daily plan generation
- Progress monitoring
- Blocker analysis
- Sprint planning

**Best for**: Staying on top of daily execution and shipping on time

---

### 4. [Stakeholder Agent](./stakeholder-agent.md)
**Focus**: Communication, alignment, relationship management
- Stakeholder mapping
- Meeting agenda/notes
- Status updates
- Influence strategies

**Best for**: Managing up, across, and maintaining alignment

---

### Coming Soon

Additional agents to complete your Personal OS:

- **Analytics Agent**: Metrics tracking, A/B testing, data insights
- **Planning Agent**: Backlog management, prioritization, roadmapping
- **Documentation Agent**: PRD creation, knowledge management
- **Learning Agent**: Continuous improvement, trend curation

---

## How to Use These Templates

### Step 1: Choose Your Starting Agent
**Recommended sequence**:
1. Start with **Execution Agent** (immediate productivity boost)
2. Add **Stakeholder Agent** (communication improvements)
3. Layer in **Strategy Agent** (alignment)
4. Integrate **Discovery Agent** (user insights)

### Step 2: Customize the Agent
Each agent template includes:
- ✅ **Configuration section**: Input/output sources to connect
- ✅ **Core prompts**: Ready-to-use AI prompts for each function
- ✅ **Workflows**: Automated trigger schedules
- ✅ **Integration checklist**: What to connect
- ✅ **Success metrics**: How to measure effectiveness

**What to customize**:
- Your specific tools (replace Jira with Linear, etc.)
- Your organization's terminology
- Your stakeholder list
- Your preferred communication style
- Your industry context

### Step 3: Set Up Integrations
Each agent lists required connections:
- Calendar systems
- Task management tools
- Communication platforms
- Data sources
- Documentation systems

### Step 4: Start Simple
**Week 1**: Use ONE prompt from the agent manually
- Copy the prompt template
- Fill in your specific inputs
- Use ChatGPT/Claude to generate output
- Evaluate the results

**Week 2**: Add ONE workflow
- Set a calendar reminder for the trigger time
- Run the workflow manually
- Refine based on results

**Week 3**: Expand
- Add more prompts
- Increase automation
- Fine-tune outputs

---

## Implementation Patterns

### Pattern 1: Manual Mode (Start Here)
```
1. Copy prompt template from agent file
2. Fill in your specific context
3. Paste into ChatGPT/Claude
4. Use the output
5. Iterate and improve
```

**Time investment**: 5-10 minutes per use
**Benefit**: Immediate value, learn what works
**Best for**: Testing before automating

---

### Pattern 2: Templated Mode
```
1. Create saved templates in your note-taking tool
2. Fill in variables each time
3. Run through AI assistant
4. Build up a library of outputs
```

**Time investment**: Setup 30 min, then 5 min per use
**Benefit**: Faster execution, consistency
**Best for**: Regular recurring tasks

---

### Pattern 3: Automated Mode (Advanced)
```
1. Connect agents to your tools via API/automation
2. Set up triggers (time-based or event-based)
3. Agent runs automatically
4. Review and adjust outputs
```

**Time investment**: Setup 2-4 hours per agent
**Benefit**: Hands-free execution
**Best for**: High-frequency workflows
**Note**: Requires automation scripts (coming next phase)

---

## Quick Start Checklist

### Before You Begin
- [ ] Read through one agent file completely
- [ ] Identify your current biggest pain point
- [ ] Choose the agent that addresses that pain
- [ ] Set aside 30 minutes for first test

### First Agent Setup (Choose One)
**Execution Agent** (if you struggle with daily planning):
- [ ] Try "Daily Plan Generator" prompt tomorrow morning
- [ ] Use output to guide your day
- [ ] Note what worked and what didn't

**Stakeholder Agent** (if you spend too much time on updates):
- [ ] Try "Status Update Generator" for next weekly update
- [ ] Compare time saved vs. manual approach
- [ ] Refine template with your terminology

**Discovery Agent** (if you have interview notes piling up):
- [ ] Use "Interview Synthesizer" on one recent interview
- [ ] Extract insights you might have missed
- [ ] Share with team to validate usefulness

**Strategy Agent** (if you feel misaligned):
- [ ] Run "Daily Strategy Check" tomorrow morning
- [ ] Review alignment score
- [ ] Adjust priorities based on output

### First Week Goals
- [ ] Use your chosen agent's primary prompt 3+ times
- [ ] Customize the prompt for your context
- [ ] Measure time saved or quality improved
- [ ] Decide: keep, modify, or try different agent

---

## Prompts Quick Reference

### Most Impactful Prompts (Start Here)

**Daily Impact**:
- Execution Agent → "Daily Plan Generator"
- Strategy Agent → "Daily Strategy Check"

**Weekly Impact**:
- Stakeholder Agent → "Status Update Generator"
- Discovery Agent → "Feedback Trend Detector"

**Monthly Impact**:
- Strategy Agent → "OKR Planning Assistant"
- Stakeholder Agent → "Stakeholder Mapping"

---

## Customization Examples

### Example: Adapting for Your Industry

**If you're in B2B SaaS**:
- Discovery Agent: Add enterprise customer feedback weighting
- Stakeholder Agent: Include customer success team in map
- Strategy Agent: Focus on ARR and expansion metrics

**If you're in B2C Mobile**:
- Discovery Agent: Emphasize app store reviews
- Analytics Agent: Focus on DAU/retention
- Strategy Agent: Viral growth and engagement focus

**If you're in Healthcare**:
- Discovery Agent: Include regulatory/compliance concerns
- Documentation Agent: Enhanced audit trail requirements
- Strategy Agent: Patient safety as top priority

### Example: Adapting for Company Stage

**Early Startup**:
- Lighter on process, heavier on speed
- Focus: Execution Agent, Discovery Agent
- Stakeholder Agent: Simplified (fewer stakeholders)

**Growth Stage**:
- Balance speed and process
- All agents relevant
- Focus on scaling patterns

**Enterprise**:
- More structure and documentation
- Stakeholder Agent critical
- Documentation Agent essential

---

## Measuring Success

### Agent Effectiveness Scorecard

After using an agent for 2 weeks, score it:

**Time Savings**: ⭐⭐⭐⭐⭐
- How much time did it save?
- 5 stars = >30% time savings

**Output Quality**: ⭐⭐⭐⭐⭐
- Was the output useful as-is?
- 5 stars = 90% usable without edits

**Consistency**: ⭐⭐⭐⭐⭐
- Does it work reliably?
- 5 stars = Works every time

**Learning Curve**: ⭐⭐⭐⭐⭐
- How easy was it to adopt?
- 5 stars = Useful from day 1

**Keep using if**: Average score > 3 stars
**Needs refinement if**: Average score 2-3 stars
**Pause if**: Average score < 2 stars (try different agent)

---

## Common Questions

### "Which agent should I start with?"
Answer: The one that addresses your current biggest pain point.
- Drowning in tasks? → Execution Agent
- Constantly misaligned? → Strategy Agent
- Too many status updates? → Stakeholder Agent
- Feedback not actionable? → Discovery Agent

### "Do I need all agents running at once?"
No! Start with one, master it, then add another. Full system might take 2-3 months to build.

### "What if the outputs aren't perfect?"
That's normal. These are templates. Customize the prompts with:
- Your company's terminology
- Your specific workflows
- Your stakeholder preferences
- Your success metrics

### "How technical do I need to be?"
**Manual mode**: No technical skills needed (copy/paste)
**Templated mode**: Basic (saving templates in Notion/Docs)
**Automated mode**: Moderate (will provide scripts in next phase)

### "Can I use these without AI tools?"
The prompts are designed for AI, but you can:
- Use them as checklists/frameworks manually
- Adapt them as document templates
- Use as thinking frameworks

But you'll get 10x value by using AI to execute them.

---

## Next Steps

### Immediate (Today)
1. Choose one agent based on your pain point
2. Read that agent's file fully
3. Pick ONE prompt to try tomorrow
4. Set a calendar reminder to use it

### This Week
1. Use that prompt 3+ times
2. Customize it for your context
3. Measure the impact
4. Decide to continue or pivot

### This Month
1. Master your first agent
2. Add a second agent
3. Start building your personal OS library
4. Prepare for automation (coming soon)

### This Quarter
1. Have 3-4 agents running smoothly
2. Customize prompts to your perfection
3. Build automation for high-frequency workflows
4. Measure productivity gains

---

## Support & Iteration

### Give Feedback
As you use these agents:
- Note what works and what doesn't
- Track your time savings
- Identify gaps or needs
- Share wins with your team

### Continuous Improvement
- Review agent effectiveness monthly
- Update prompts based on learnings
- Add new prompts as needs emerge
- Refine workflows for efficiency

---

## Resources

### In This Directory
- `strategy-agent.md` - Strategic planning and alignment
- `discovery-agent.md` - User research and insights
- `execution-agent.md` - Task management and delivery
- `stakeholder-agent.md` - Communication and relationships

### Coming Next
- Automation scripts for each agent
- Integration tutorials
- Example outputs and case studies
- Advanced customization guides

---

## Quick Win Recipes

### Recipe 1: "Never Write a Status Update from Scratch Again"
**Time**: 30 minutes setup, 5 min per use
**Agent**: Stakeholder Agent
**Prompt**: "Status Update Generator"
**Steps**:
1. Create template in Google Docs
2. Fill in your project metrics
3. Run through AI
4. Send to stakeholders
**Expected result**: 70% time savings on updates

### Recipe 2: "Always Know Your Top 3 Priorities"
**Time**: 20 minutes setup, 5 min per day
**Agent**: Execution Agent
**Prompt**: "Daily Plan Generator"
**Steps**:
1. Every morning at 8 AM
2. List your open tasks
3. Run through AI
4. Follow the plan
**Expected result**: 25% more focus time

### Recipe 3: "Turn Interviews into Gold"
**Time**: 15 minutes per interview
**Agent**: Discovery Agent
**Prompt**: "Interview Synthesizer"
**Steps**:
1. Record or take notes in interview
2. Run notes through AI
3. Extract insights and actions
4. Share with team
**Expected result**: 3x more insights captured

### Recipe 4: "Strategic Alignment Every Day"
**Time**: 5 minutes per day
**Agent**: Strategy Agent
**Prompt**: "Daily Strategy Check"
**Steps**:
1. Morning ritual after coffee
2. List today's planned tasks
3. Check against OKRs
4. Adjust priorities
**Expected result**: >80% strategic alignment

---

**Ready to build your Personal OS? Pick an agent and start today!**
