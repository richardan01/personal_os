# Personal OS - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         PERSONAL OS                             │
│                    (Python Automation System)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│   AI Engine  │      │  Integrations│     │   Scheduler  │
│              │      │              │     │              │
│ Claude/GPT   │      │  • Slack     │     │  • Daily     │
│              │      │  • Calendar  │     │  • Weekly    │
│ Generates:   │      │  • Tasks     │     │  • Triggers  │
│ • Plans      │      │  • CRM       │     │              │
│ • Summaries  │      │              │     │              │
│ • Insights   │      │              │     │              │
└──────────────┘      └──────────────┘     └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │     4 Agents     │
                    │                  │
                    │  1. Execution    │
                    │  2. Strategy     │
                    │  3. Discovery    │
                    │  4. Stakeholder  │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Slack (You)    │
                    │                  │
                    │  Daily updates   │
                    │  in DMs          │
                    └──────────────────┘
```

---

## 🔄 Data Flow

### Morning Daily Plan Workflow

```
1. TRIGGER (8:00 AM)
   │
   ├─→ main.py (scheduler)
   │
2. FETCH DATA
   │
   ├─→ Calendar API → Today's meetings
   ├─→ Task System → Open tasks & deadlines
   └─→ Config → Strategic priorities
   │
3. GENERATE PLAN
   │
   ├─→ execution_agent.py
   │   │
   │   └─→ ai_client.py
   │       │
   │       └─→ Anthropic/OpenAI API
   │           │
   │           └─→ Generated Daily Plan (text)
   │
4. SEND TO USER
   │
   └─→ slack_client.py
       │
       └─→ Slack API
           │
           └─→ Your DM with daily plan
```

---

## 📦 Component Details

### Core Components

#### 1. **main.py** - Orchestrator
```python
Responsibilities:
- Initialize all agents
- Setup schedules
- Coordinate workflows
- Handle errors
- Logging

Key Functions:
- setup_schedules()
- run_morning_daily_plan()
- run_midday_progress_check()
- run_evening_summary()
```

#### 2. **config.py** - Configuration
```python
Responsibilities:
- Load environment variables
- Validate configuration
- Provide settings to all modules

Key Settings:
- API keys
- Schedule times
- Personal context
- Feature flags
```

#### 3. **ai_client.py** - AI Interface
```python
Responsibilities:
- Unified API for Claude/GPT
- Handle prompt generation
- Manage API calls
- Error handling

Supports:
- Anthropic Claude
- OpenAI GPT
- Temperature control
- Token limits
```

#### 4. **slack_client.py** - Slack Interface
```python
Responsibilities:
- Send messages to Slack
- Format rich messages
- Handle channels/DMs
- Error recovery

Functions:
- send_message()
- send_dm()
- send_formatted_message()
- send_daily_plan()
- send_alert()
```

---

## 🤖 Agent Architecture

### Agent Pattern

Each agent follows this structure:

```python
class Agent:
    def __init__(self):
        # Initialize agent

    def generate_[workflow](self, inputs):
        # Build prompt with context
        # Call AI client
        # Return generated content

    def send_to_slack(self, content):
        # Format for Slack
        # Send via slack_client
```

### Execution Agent Flow

```
Input Sources          Agent Logic           Output Destinations
─────────────         ──────────────        ───────────────────

Calendar Events  ──┐
                   │
Open Tasks       ──┤──→ Build Context  ──→  Generate     ──→  Slack DM
                   │    with Prompt         Daily Plan
Priorities       ──┤
                   │
Yesterday Data   ──┘
```

---

## 🔌 Integration Points

### Current Integrations

```
┌────────────────┐
│  Slack Bot     │ ──→ Receives all outputs
│                │ ──→ Can trigger workflows (future)
└────────────────┘

┌────────────────┐
│  AI Provider   │ ──→ Claude or OpenAI
│  (Claude/GPT)  │ ──→ Generates all text
└────────────────┘
```

### Future Integrations

```
┌────────────────┐
│ Google Calendar│ ──→ Fetch meetings/events
│                │ ──→ Block focus time
└────────────────┘

┌────────────────┐
│ Notion/Jira    │ ──→ Fetch tasks
│                │ ──→ Update status
│                │ ──→ Create tasks
└────────────────┘

┌────────────────┐
│ Analytics      │ ──→ Fetch metrics
│ (Mixpanel)     │ ──→ Track KPIs
└────────────────┘
```

---

## 📅 Scheduling System

### Schedule Architecture

```python
# Built on 'schedule' library

schedule.every().day.at("08:00").do(workflow_function)
schedule.every().monday.at("09:00").do(weekly_function)

# Main loop
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

### Schedule Registry

| Schedule Type | Example | Use Case |
|--------------|---------|----------|
| Daily at time | `every().day.at("08:00")` | Morning plan |
| Weekday at time | `every().monday.at("09:00")` | Weekly review |
| Interval | `every(2).hours` | Periodic check |
| Immediate | `run_pending()` | Manual trigger |

---

## 🔐 Security Architecture

### Secrets Management

```
.env (Local Development)
├── API Keys (encrypted at rest)
├── Tokens (never committed to git)
└── Personal data

Production (Future)
├── AWS Secrets Manager
├── Environment variables
└── Encrypted config files
```

### Access Control

```
Slack Bot Scopes:
├── chat:write (Send messages)
├── users:read (Get user info)
├── channels:read (List channels)
└── im:write (Send DMs)

API Permissions:
├── AI: Read-only (no training on data)
└── Calendar: Read-only (fetch events)
```

---

## 📊 State Management

### Current State (Stateless)

```
Each workflow is independent:
- No persistent database
- Fresh context each run
- Logs stored in files
```

### Future State (Stateful)

```
┌─────────────────┐
│   SQLite DB     │
│                 │
│ • Agent history │
│ • Task cache    │
│ • Metrics log   │
│ • User prefs    │
└─────────────────┘
```

---

## 🚀 Deployment Options

### Option 1: Local Machine (Current)
```
Your Computer
├── Always on
├── Python script running
└── Checks schedule every minute
```

**Pros**: Free, simple, full control
**Cons**: Computer must stay on

### Option 2: Cloud Server (Production)
```
AWS EC2 / DigitalOcean Droplet
├── t2.micro instance ($5-10/month)
├── Runs as systemd service
└── Auto-restart on failure
```

**Pros**: Always available, reliable
**Cons**: Small monthly cost

### Option 3: Serverless (Advanced)
```
AWS Lambda + EventBridge
├── Triggered by CloudWatch Events
├── Pay per execution
└── No server management
```

**Pros**: Minimal cost, scalable
**Cons**: More complex setup

---

## 🔧 Configuration Flow

```
1. .env file
   │
   ▼
2. config.py loads & validates
   │
   ▼
3. Settings object created
   │
   ▼
4. All modules import settings
   │
   ▼
5. Runtime: Settings used everywhere
```

---

## 📈 Scalability

### Current Scale
- 1 user (you)
- 4 agents
- ~10 workflows/day
- Minimal resource usage

### Future Scale
```
Multi-User:
├── User database
├── Per-user config
├── Isolated workflows
└── Admin dashboard

Multi-Agent:
├── Agent marketplace
├── Custom agent builder
├── Agent collaboration
└── Swarm intelligence
```

---

## 🧪 Testing Strategy

### Unit Tests (Future)
```python
tests/
├── test_execution_agent.py
├── test_ai_client.py
├── test_slack_client.py
└── test_config.py
```

### Integration Tests (Future)
```python
# Test full workflow
def test_morning_plan_workflow():
    # Mock calendar
    # Mock task system
    # Run workflow
    # Verify Slack message
```

### Manual Testing (Current)
```bash
# Test each component
python config.py
python utils/ai_client.py
python utils/slack_client.py
python agents/execution_agent.py
```

---

## 📝 Error Handling

### Error Flow

```
Error Occurs
│
├─→ Logged to file (logs/personal_os.log)
│
├─→ Slack alert sent (if critical)
│
└─→ Graceful degradation
    │
    ├─→ Retry (if transient)
    ├─→ Skip (if non-critical)
    └─→ Halt (if critical)
```

### Error Categories

| Level | Action | Example |
|-------|--------|---------|
| DEBUG | Log only | Verbose info |
| INFO | Log only | Workflow started |
| WARNING | Log + continue | API slow |
| ERROR | Log + alert | API failed |
| CRITICAL | Log + alert + halt | Config invalid |

---

## 🔄 Update & Maintenance

### Version Control
```
Git Repository
├── main branch (stable)
├── develop branch (testing)
└── feature/* branches
```

### Update Process
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart system
python main.py
```

---

## 📱 Future Enhancements

### Phase 2: Enhanced Agents
```
+ Strategy Agent (OKR tracking)
+ Discovery Agent (Feedback analysis)
+ Stakeholder Agent (Communication)
+ Analytics Agent (Metrics)
```

### Phase 3: Advanced Features
```
+ Dashboard (web UI)
+ Mobile app
+ Voice interface
+ Team collaboration
+ API for custom integrations
```

---

## 🎯 Success Metrics

### System Health
- Uptime: Target 99%
- Workflow success rate: Target 95%
- Response time: Target < 30s

### User Value
- Time saved: Target 30%+
- Task completion: Target 85%+
- User satisfaction: Target 4.5/5

---

## 🤝 Contributing

### Adding a New Component

1. Create file in appropriate directory
2. Follow existing patterns
3. Add configuration to .env.example
4. Document in README
5. Add tests
6. Submit PR

### Code Style
- Python 3.9+
- Type hints encouraged
- Docstrings for all functions
- Follow PEP 8

---

**This architecture is designed to be simple, maintainable, and extensible. Start simple, add complexity as needed.**
