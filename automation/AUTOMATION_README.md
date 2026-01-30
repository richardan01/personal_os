# Personal OS - Automation System

Automate your product management workflows with AI-powered agents that help you plan, execute, and communicate more effectively.

---

## What This Does

Your Personal OS runs in the background and:

- **8:00 AM**: Sends you a prioritized daily plan based on your calendar and tasks
- **12:30 PM**: Checks your progress and suggests adjustments
- **5:30 PM**: Summarizes your day and prepares tomorrow's priorities
- **Weekly**: Runs stakeholder discovery to analyze meeting notes and build profiles
- **Continuous**: Processes feedback and insights as they arrive

All outputs are saved to Google Docs for easy reference and sharing.

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Configuration
```bash
cp .env.example .env
# Edit .env with your API keys and Google Workspace credentials
```

### 3. Run the System
```bash
python main.py
```

**For detailed setup instructions, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)**

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         PERSONAL OS                             │
│                    (Python Automation System)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐     ┌──────────────┐
│   AI Engine  │      │  Integrations│     │   Scheduler  │
│              │      │              │     │              │
│ Claude/GPT   │      │  • Google    │     │  • Daily     │
│              │      │    Workspace │     │  • Weekly    │
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
                    │      Agents      │
                    │                  │
                    │  • Execution     │
                    │  • Strategy      │
                    │  • Discovery     │
                    │  • Stakeholder   │
                    │    Discovery     │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Google Docs     │
                    │                  │
                    │  Reports &       │
                    │  Updates         │
                    └──────────────────┘
```

### Data Flow - Stakeholder Discovery Workflow

```
1. TRIGGER (Weekly or On-Demand)
   │
   ├─→ main.py (scheduler)
   │
2. SEARCH & FETCH DOCUMENTS
   │
   ├─→ Document Search Skill → Google Drive
   │   └─→ Find meeting notes, PRDs, interview transcripts
   │
   ├─→ Document Reader Skill → Google Docs/Sheets/Slides
   │   └─→ Extract content from found documents
   │
3. AI-POWERED SYNTHESIS
   │
   ├─→ Note Synthesis Skill
   │   └─→ Claude extracts stakeholder insights
   │       • Names, roles, concerns, needs
   │       • Quotes, sentiment, priorities
   │
4. BUILD PROFILES & RELATIONSHIPS
   │
   ├─→ Stakeholder Profiler Skill
   │   └─→ Create/update stakeholder profiles
   │
   ├─→ Relationship Mapper Skill
   │   └─→ Map influence and connections
   │
5. AGGREGATE & REPORT
   │
   ├─→ Insight Aggregator Skill
   │   └─→ Find patterns across stakeholders
   │
   ├─→ Task Creator Skill → Google Tasks
   │   └─→ Create follow-up action items
   │
   └─→ Report Generator Skill → Google Docs
       └─→ Generate stakeholder analysis report
```

---

## Available Agents

### Execution Agent
- Daily plan generation
- Progress tracking
- Daily summaries
- Blocker management

**Status**: ✅ Fully implemented

### Strategy Agent
- Daily strategy alignment
- OKR tracking
- Competitive analysis
- Roadmap reviews

**Status**: ✅ Fully implemented

### Discovery Agent
- Feedback synthesis
- Interview analysis
- Trend detection
- Feature request prioritization

**Status**: ✅ Fully implemented

### Planning Agent
- Backlog management and prioritization
- Sprint planning
- RICE prioritization
- Capacity planning

**Status**: ✅ Fully implemented

### Stakeholder Agent
- Scans meeting notes and documents in Google Drive
- Extracts stakeholder insights using AI
- Builds and maintains stakeholder profiles
- Maps relationships and influence
- Creates follow-up tasks in Google Tasks
- Generates comprehensive reports in Google Docs

**Status**: ✅ Fully implemented

### Analytics Agent
- Metrics tracking
- A/B test analysis
- Performance monitoring
- Data-driven decision making

**Status**: ✅ Fully implemented

### Documentation Agent
- PRD creation and maintenance
- Decision log tracking
- Meeting notes organization
- Wiki/knowledge base management

**Status**: ✅ Fully implemented

### Learning Agent
- Industry trend curation
- Best practice recommendations
- Skill gap identification
- Learning resource curation
- Retrospective facilitation

**Status**: ✅ Fully implemented

---

## Skills Architecture

Skills are stateless, reusable building blocks that agents combine to accomplish complex workflows.

### Skill Pattern

```python
class Skill:
    """
    Skills are stateless, reusable building blocks.
    They perform one specific task well.
    """

    def __init__(self, clients: Dict[str, Any]):
        # Inject required clients (Google, AI, etc.)

    def execute(self, inputs: Dict) -> Dict:
        # Perform the skill's specific task
        # Return structured results
```

### Available Skills

| Skill | Purpose | Input | Output |
|-------|---------|-------|--------|
| DocumentSearch | Find docs in Drive | Query, filters | List of file IDs |
| DocumentReader | Extract content | File ID, doc type | DocumentContent |
| NoteSynthesis | AI extraction | Raw text | StakeholderInsights |
| StakeholderProfiler | Build profiles | Insights | StakeholderProfiles |
| RelationshipMapper | Map connections | Profiles | InfluenceMatrix |
| InsightAggregator | Find patterns | All insights | Themes, conflicts |
| TaskCreator | Create tasks | Action items | Task IDs |
| ReportGenerator | Generate reports | All data | Doc ID |

---

## Data Models

### Model Architecture

```
models/
├── enums.py          # DocType, Sentiment, Priority, InfluenceLevel, Stance
├── document.py       # DocumentContent, TableData
├── insight.py        # Concern, Need, Quote, Theme, Conflict
├── stakeholder.py    # StakeholderInsight, StakeholderProfile
├── relationship.py   # Relationship, InfluenceMatrix, StakeholderCluster
├── action.py         # ActionItem, InteractionSummary
└── report.py         # InsightSummary, DiscoveryReport
```

### Key Data Classes

```python
@dataclass
class StakeholderProfile:
    name: str
    role: str
    department: str
    influence_level: InfluenceLevel
    concerns: List[Concern]
    needs: List[Need]
    quotes: List[Quote]
    relationships: List[Relationship]
    engagement_history: List[InteractionSummary]
    action_items: List[ActionItem]
```

---

## Google Workspace Integration

### Client Architecture

```
utils/google/
├── base_client.py      # OAuth2/Service Account auth
├── drive_client.py     # File storage and search
├── docs_client.py      # Document creation and reading
├── sheets_client.py    # Spreadsheet operations
├── slides_client.py    # Presentation management
├── calendar_client.py  # Event and scheduling
└── tasks_client.py     # Task management
```

### Authentication Flow

```
1. Load Credentials
   │
   ├─→ Service Account (for server-to-server)
   │   └─→ GOOGLE_SERVICE_ACCOUNT_FILE
   │
   └─→ OAuth2 (for user-specific access)
       └─→ GOOGLE_CREDENTIALS_FILE
           │
           └─→ Token storage/refresh
```

### API Scopes

```python
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks',
]
```

---

## Project Structure

```
automation/
├── main.py                    # Main automation runner
├── config.py                  # Configuration management
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
├── SETUP_GUIDE.md            # Detailed setup instructions
├── AUTOMATION_README.md      # This file
│
├── agents/                    # AI agents (orchestrators)
│   ├── execution_agent.py    # Daily planning & tracking
│   ├── stakeholder_discovery_agent.py  # Stakeholder analysis
│   ├── strategy_agent.py     # Coming soon
│   └── discovery_agent.py    # Coming soon
│
├── skills/                    # Reusable skill modules
│   ├── document_search.py    # Search Google Drive
│   ├── document_reader.py    # Read Docs/Sheets/Slides
│   ├── note_synthesis.py     # AI-powered extraction
│   ├── stakeholder_profiler.py  # Build profiles
│   ├── relationship_mapper.py   # Map influence
│   ├── insight_aggregator.py    # Find patterns
│   ├── task_creator.py       # Create Google Tasks
│   └── report_generator.py   # Generate reports
│
├── models/                    # Data models
│   ├── enums.py              # Enumerations
│   ├── document.py           # Document models
│   ├── insight.py            # Insight models
│   ├── stakeholder.py        # Stakeholder models
│   ├── relationship.py       # Relationship models
│   ├── action.py             # Action item models
│   └── report.py             # Report models
│
├── utils/                     # Utility modules
│   ├── ai_client.py          # AI provider interface
│   └── google/               # Google Workspace clients
│       ├── base_client.py    # Auth handling
│       ├── drive_client.py   # Google Drive
│       ├── docs_client.py    # Google Docs
│       ├── sheets_client.py  # Google Sheets
│       ├── slides_client.py  # Google Slides
│       ├── calendar_client.py # Google Calendar
│       └── tasks_client.py   # Google Tasks
│
├── integrations/              # Third-party integrations
│   ├── notion.py             # Coming soon
│   ├── jira.py               # Coming soon
│   └── asana.py              # Coming soon
│
└── logs/                      # Application logs
    └── personal_os.log
```

---

## Configuration

All configuration is done via environment variables in `.env`:

### Required
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` - AI provider
- `GOOGLE_CREDENTIALS_FILE` - Path to Google OAuth credentials
- `GOOGLE_CALENDAR_ID` - Your Google Calendar ID

### Optional
- `GOOGLE_SERVICE_ACCOUNT_FILE` - For service account auth
- `GOOGLE_DRIVE_FOLDER_ID` - Folder for stakeholder documents
- `GOOGLE_TASKS_LIST_ID` - Task list for action items
- `NOTION_API_KEY` - For Notion integration
- `JIRA_URL` - For Jira integration

See `.env.example` for all options.

---

## Scheduling System

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

### Default Schedule

| Time | Workflow | Agent |
|------|----------|-------|
| 8:00 AM | Daily Plan | Execution |
| 12:30 PM | Progress Check | Execution |
| 5:30 PM | Daily Summary | Execution |
| Friday 3:00 PM | Stakeholder Discovery | Stakeholder Discovery |

Customize in `.env`:
```bash
EXECUTION_AGENT_MORNING_TIME=09:00
EXECUTION_AGENT_MIDDAY_TIME=13:00
EXECUTION_AGENT_EVENING_TIME=18:00
```

---

## Usage Examples

### Run in Dry Run Mode
Test without saving actual documents:
```bash
# In .env
DRY_RUN=true

python main.py
```

### Run a Specific Agent Manually
```bash
python agents/execution_agent.py
python agents/stakeholder_discovery_agent.py
```

### Test Components
```bash
# Test configuration
python config.py

# Test AI client
python utils/ai_client.py

# Test Google clients
python utils/google/drive_client.py
```

---

## Example Output

### Stakeholder Discovery Report (Google Doc)

```
# Stakeholder Discovery Report
Generated: 2026-01-26

## Executive Summary
Analyzed 15 documents, identified 8 stakeholders across 3 departments.

## Key Stakeholders

### Sarah Chen - VP of Engineering
- **Influence Level**: High
- **Stance**: Supportive
- **Top Concerns**:
  - Technical debt in authentication system
  - Team capacity for Q2 roadmap
- **Key Quotes**:
  "We need at least 2 sprints to properly address the auth issues"
- **Recommended Actions**:
  - Schedule technical deep-dive meeting
  - Share Q2 capacity planning doc

### Mike Johnson - Sales Director
- **Influence Level**: High
- **Stance**: Neutral
...

## Relationship Map
[Influence matrix showing connections between stakeholders]

## Recommended Follow-ups
1. [ ] Schedule 1:1 with Sarah Chen re: auth concerns
2. [ ] Share roadmap draft with Mike Johnson
3. [ ] Prepare executive summary for leadership sync
```

---

## Integrations

### Current
- Google Workspace (Drive, Docs, Sheets, Slides, Calendar, Tasks)
- Anthropic Claude (AI)
- OpenAI GPT (AI alternative)

### Coming Soon
- Notion
- Jira
- Linear
- Asana

---

## Deployment

### Option 1: Local Machine (Development)
```bash
python main.py
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

### Option 3: Serverless (Advanced)
```
AWS Lambda + EventBridge
├── Triggered by CloudWatch Events
├── Pay per execution
└── No server management
```

### Run in Background
```bash
# Using nohup (Linux/Mac)
nohup python main.py > output.log 2>&1 &

# Using screen (Linux/Mac)
screen -S personal-os
python main.py
# Press Ctrl+A then D to detach
```

---

## Security

### Secrets Management

```
.env (Local Development)
├── API Keys (encrypted at rest)
├── Tokens (never committed to git)
├── Google credentials path
└── Personal data

Production
├── AWS Secrets Manager
├── Environment variables
└── Encrypted config files
```

### Best Practices
- Never commit `.env` file (already in `.gitignore`)
- Use environment variables for secrets
- Rotate API keys regularly
- Review logs for sensitive data before sharing
- Use read-only permissions where possible

---

## Logging

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

## Error Handling

### Error Flow

```
Error Occurs
│
├─→ Logged to file (logs/personal_os.log)
│
├─→ Alert generated (if critical)
│
└─→ Graceful degradation
    │
    ├─→ Retry (if transient)
    ├─→ Skip (if non-critical)
    └─→ Halt (if critical)
```

---

## Troubleshooting

### Common Issues

**"Configuration validation failed"**
- Check your `.env` file has all required fields
- Verify API keys are correct
- Ensure Google credentials file exists

**"Google API error: invalid credentials"**
- Re-run OAuth flow to refresh tokens
- Check service account permissions
- Verify API is enabled in Google Cloud Console

**"No documents found"**
- Check `GOOGLE_DRIVE_FOLDER_ID` is correct
- Ensure service account has access to the folder
- Try broader search terms

**"Module not found"**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for more troubleshooting.

---

## Contributing

### Adding a New Agent

1. Create agent file: `agents/your_agent.py`
2. Implement agent class following the pattern
3. Add workflow in `main.py`
4. Add schedule in `setup_schedules()`
5. Test thoroughly

### Adding a Skill

1. Create skill file: `skills/your_skill.py`
2. Implement skill class following the pattern
3. Add to agent that needs it
4. Document in README
5. Add tests

### Code Style
- Python 3.9+
- Type hints encouraged
- Docstrings for all functions
- Follow PEP 8

---

## Roadmap

### Phase 1: Core Execution (Complete)
- [x] Execution Agent
- [x] Google Workspace integration
- [x] AI client (Claude/OpenAI)
- [x] Scheduling system
- [x] Stakeholder Discovery Agent
- [x] Skills architecture

### Phase 2: Enhanced Intelligence (Complete)
- [x] Strategy Agent
- [x] Discovery Agent
- [x] Planning Agent
- [x] Stakeholder Agent
- [x] Analytics Agent
- [x] Documentation Agent
- [x] Learning Agent
- [ ] Task system integrations (Notion, Jira)

### Phase 3: Advanced Features
- [ ] Analytics dashboard
- [ ] Multi-user support
- [ ] Custom workflows builder
- [ ] Mobile app
- [ ] Voice interface

---

## Resources

- [Detailed Setup Guide](./SETUP_GUIDE.md)
- [Integration Guide](./INTEGRATION_GUIDE.md)
- [Agent Implementation Templates](./agents/)

---

## Success Stories

Once running, you can expect:
- **30%+ time savings** on planning and status updates
- **Better stakeholder relationships** with organized insights
- **No missed priorities** with automated planning
- **Consistent communication** with stakeholders
- **More focus time** by automating routine tasks

---

## License

This is a personal productivity tool. Use and modify as needed for your own workflow.

---

## Support

For questions or issues:
1. Check [SETUP_GUIDE.md](./SETUP_GUIDE.md)
2. Review logs in `logs/personal_os.log`
3. Test components individually
4. Check `.env` configuration

---

**Built for Product Managers who want to focus on building great products, not managing tasks.**
