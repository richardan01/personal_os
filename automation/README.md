# Personal OS - Automation System

Automate your product management workflows with AI-powered agents that help you plan, execute, and communicate more effectively.

---

## 🎯 What This Does

Your Personal OS runs in the background and:

- **8:00 AM**: Sends you a prioritized daily plan based on your calendar and tasks
- **12:30 PM**: Checks your progress and suggests adjustments
- **5:30 PM**: Summarizes your day and prepares tomorrow's priorities
- **Weekly**: Generates status updates for stakeholders
- **Continuous**: Processes feedback and insights as they arrive

All delivered directly to your Slack DMs.

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Configuration
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the System
```bash
python main.py
```

**👉 For detailed setup instructions, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)**

---

## 🤖 Available Agents

### Execution Agent ✅
- Daily plan generation
- Progress tracking
- Daily summaries
- Blocker management

**Status**: ✅ Fully implemented

### Strategy Agent 🎯
- Daily strategy alignment
- OKR tracking
- Competitive analysis
- Roadmap reviews

**Status**: 🚧 Coming soon

### Discovery Agent 💡
- Feedback synthesis
- Interview analysis
- Trend detection
- Feature request prioritization

**Status**: 🚧 Coming soon

### Stakeholder Agent 📊
- Meeting agendas/notes
- Status updates
- Stakeholder mapping
- Communication management

**Status**: 🚧 Coming soon

---

## 📁 Project Structure

```
automation/
├── main.py                    # Main automation runner
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── SETUP_GUIDE.md            # Detailed setup instructions
├── README.md                 # This file
│
├── agents/                    # AI agents
│   ├── execution_agent.py    # Daily planning & tracking
│   ├── strategy_agent.py     # Coming soon
│   ├── discovery_agent.py    # Coming soon
│   └── stakeholder_agent.py  # Coming soon
│
├── utils/                     # Utility modules
│   ├── ai_client.py          # AI provider interface
│   ├── slack_client.py       # Slack integration
│   ├── calendar_client.py    # Coming soon
│   └── task_client.py        # Coming soon
│
├── integrations/              # Third-party integrations
│   ├── notion.py             # Coming soon
│   ├── jira.py               # Coming soon
│   └── google_calendar.py    # Coming soon
│
└── logs/                      # Application logs
    └── personal_os.log
```

---

## 🔧 Configuration

All configuration is done via environment variables in `.env`:

### Required
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` - AI provider
- `SLACK_BOT_TOKEN` - Slack bot token
- `SLACK_USER_ID` - Your Slack user ID

### Optional
- `NOTION_API_KEY` - For task integration
- `JIRA_URL` - For Jira integration
- `GOOGLE_CALENDAR_CREDENTIALS` - For calendar integration

See `.env.example` for all options.

---

## 🚀 Usage Examples

### Run in Dry Run Mode
Test without sending actual messages:
```bash
# In .env
DRY_RUN=true

python main.py
```

### Run a Specific Agent Manually
```bash
python agents/execution_agent.py
```

### Test Components
```bash
# Test configuration
python config.py

# Test AI client
python utils/ai_client.py

# Test Slack client
python utils/slack_client.py
```

---

## ⏰ Default Schedule

| Time | Workflow | Agent |
|------|----------|-------|
| 8:00 AM | Daily Plan | Execution |
| 12:30 PM | Progress Check | Execution |
| 5:30 PM | Daily Summary | Execution |
| Friday 3:00 PM | Weekly Update | Stakeholder |

Customize in `.env`:
```bash
EXECUTION_AGENT_MORNING_TIME=09:00
EXECUTION_AGENT_MIDDAY_TIME=13:00
EXECUTION_AGENT_EVENING_TIME=18:00
```

---

## 🔌 Integrations

### Current
- ✅ Slack (messaging)
- ✅ Anthropic Claude (AI)
- ✅ OpenAI GPT (AI alternative)

### Coming Soon
- 🚧 Google Calendar
- 🚧 Notion
- 🚧 Jira
- 🚧 Linear
- 🚧 Asana

---

## 📊 Example Output

### Daily Plan (Slack DM)
```
📋 Your Daily Plan

## Daily Execution Plan - 2026-01-01

### Top 3 Priorities:
1. Complete PRD for Feature X - Links to Q1 OKR - 4h
2. Review design mockups - Unblocks designer - 1h
3. Team standup preparation - 15m

### Time-Blocked Schedule:
8:00-9:00 AM: [FOCUS] PRD Writing
9:00-9:15 AM: Team Standup
...

### Success Criteria:
✅ PRD 80% complete
✅ Design feedback provided
✅ All urgent emails handled
```

---

## 🛠️ Customization

### Modify Agent Prompts
Edit prompts in `agents/execution_agent.py`:
```python
prompt = f"""
ROLE: Personal Chief of Staff
CONTEXT: Planning optimal workday

# Add your customizations here
"""
```

### Add Custom Workflows
In `main.py`:
```python
def run_custom_workflow(self):
    """Your custom workflow"""
    # Your code here
    pass

# Schedule it
schedule.every().day.at("10:00").do(self.run_custom_workflow)
```

### Change AI Model
In `.env`:
```bash
AI_MODEL=claude-opus-4-5-20251101  # For Claude
# or
AI_MODEL=gpt-4-turbo-preview  # For OpenAI
```

---

## 📝 Logging

Logs are written to `logs/personal_os.log`:

```bash
# View logs (live)
tail -f logs/personal_os.log

# View last 100 lines
tail -n 100 logs/personal_os.log

# Search logs
grep "ERROR" logs/personal_os.log
```

Log levels (set in `.env`):
- `DEBUG` - Verbose logging
- `INFO` - Standard logging (default)
- `WARNING` - Warnings only
- `ERROR` - Errors only

---

## 🐛 Troubleshooting

### Common Issues

**"Configuration validation failed"**
- Check your `.env` file has all required fields
- Verify API keys are correct

**"Slack API error: invalid_auth"**
- Regenerate your Slack bot token
- Make sure bot is installed to workspace

**"No messages received"**
- Check `DRY_RUN=false` in `.env`
- Verify bot has `chat:write` scope
- Check bot is in channel (if sending to channel)

**"Module not found"**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for more troubleshooting.

---

## 🚢 Deployment

### Run Locally (Development)
```bash
python main.py
```

### Run in Background (Production)
```bash
# Using nohup (Linux/Mac)
nohup python main.py > output.log 2>&1 &

# Using screen (Linux/Mac)
screen -S personal-os
python main.py
# Press Ctrl+A then D to detach

# Using Windows Task Scheduler
# See SETUP_GUIDE.md for instructions
```

### Deploy to Cloud
- **AWS EC2**: Run on small instance with cron
- **DigitalOcean Droplet**: Run as systemd service
- **Heroku**: Deploy as worker dyno
- **Railway/Render**: Deploy as background worker

---

## 🔒 Security

### Best Practices
- ✅ Never commit `.env` file (already in `.gitignore`)
- ✅ Use environment variables for secrets
- ✅ Rotate API keys regularly
- ✅ Review logs for sensitive data before sharing
- ✅ Use read-only permissions where possible

### Secrets Management
```bash
# .env is gitignored
# For team sharing, use:
# - 1Password / LastPass
# - AWS Secrets Manager
# - HashiCorp Vault
```

---

## 🤝 Contributing

### Adding a New Agent

1. Create agent file: `agents/your_agent.py`
2. Implement agent class with methods
3. Add workflow in `main.py`
4. Add schedule in `setup_schedules()`
5. Test thoroughly

### Adding an Integration

1. Create integration file: `integrations/service.py`
2. Implement API client
3. Add config variables to `.env.example`
4. Document in README
5. Add tests

---

## 📚 Resources

- [Detailed Setup Guide](./SETUP_GUIDE.md)
- [Agent Implementation Templates](../agents/)
- [Personal OS Design Doc](../personal-os-design.md)

---

## 🎯 Roadmap

### Phase 1: Core Execution ✅
- [x] Execution Agent
- [x] Slack integration
- [x] AI client (Claude/OpenAI)
- [x] Scheduling system

### Phase 2: Enhanced Intelligence 🚧
- [ ] Strategy Agent
- [ ] Discovery Agent
- [ ] Stakeholder Agent
- [ ] Calendar integration
- [ ] Task system integration

### Phase 3: Advanced Features 📋
- [ ] Analytics dashboard
- [ ] Multi-user support
- [ ] Custom workflows builder
- [ ] Mobile app
- [ ] Voice interface

---

## 📄 License

This is a personal productivity tool. Use and modify as needed for your own workflow.

---

## 💬 Support

For questions or issues:
1. Check [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. Review logs in `logs/personal_os.log`
3. Test components individually
4. Check `.env` configuration

---

## 🎉 Success Stories

Once running, you can expect:
- **30%+ time savings** on planning and status updates
- **Better strategic alignment** with daily checks
- **No missed priorities** with automated planning
- **Consistent communication** with stakeholders
- **More focus time** by automating routine tasks

---

**Built with ❤️ for Product Managers who want to focus on building great products, not managing tasks.**
