# Personal OS - System Architecture

## High-Level Architecture

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
                    │     5 Agents     │
                    │                  │
                    │  1. Execution    │
                    │  2. Strategy     │
                    │  3. Discovery    │
                    │  4. Stakeholder  │
                    │  5. Stakeholder  │
                    │     Discovery    │
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

---

## Data Flow

### Morning Daily Plan Workflow

```
1. TRIGGER (8:00 AM)
   │
   ├─→ main.py (scheduler)
   │
2. FETCH DATA
   │
   ├─→ Google Calendar API → Today's meetings
   ├─→ Google Tasks API → Open tasks & deadlines
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
4. SAVE OUTPUT
   │
   └─→ Google Docs
       │
       └─→ Daily plan document created
```

### Stakeholder Discovery Workflow

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

## Component Details

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
- run_weekly_stakeholder_discovery()
```

#### 2. **config.py** - Configuration
```python
Responsibilities:
- Load environment variables
- Validate configuration
- Provide settings to all modules

Key Settings:
- API keys
- Google Workspace credentials
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

## Skills Architecture

### Skill Pattern

Each skill follows this structure:

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

## Agent Architecture

### Agent Pattern

Each agent follows this structure:

```python
class Agent:
    """
    Agents are orchestrators that combine skills
    to accomplish complex workflows.
    """

    def __init__(self):
        # Initialize required skills

    def run_workflow(self, inputs):
        # Orchestrate multiple skills
        # Handle state and errors
        # Return final results
```

### Stakeholder Discovery Agent

```
StakeholderDiscoveryAgent
│
├── Skills Used:
│   ├── DocumentSearchSkill
│   ├── DocumentReaderSkill
│   ├── NoteSynthesisSkill
│   ├── StakeholderProfilerSkill
│   ├── RelationshipMapperSkill
│   ├── InsightAggregatorSkill
│   ├── TaskCreatorSkill
│   └── ReportGeneratorSkill
│
├── Workflow Steps:
│   1. Search for relevant documents
│   2. Read and extract content
│   3. Synthesize stakeholder insights (AI)
│   4. Build/update stakeholder profiles
│   5. Map relationships and influence
│   6. Aggregate insights across stakeholders
│   7. Create follow-up tasks
│   8. Generate comprehensive report
│
└── Outputs:
    ├── StakeholderProfiles (Dict)
    ├── InfluenceMatrix (Object)
    ├── ActionItems (List)
    └── Report (Google Doc URL)
```

---

## Data Models

### Model Architecture

```
models/
├── enums.py          # DocType, Sentiment, Priority, etc.
├── document.py       # DocumentContent, TableData
├── insight.py        # Concern, Need, Quote, Theme
├── stakeholder.py    # StakeholderInsight, StakeholderProfile
├── relationship.py   # Relationship, InfluenceMatrix
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

### Schedule Registry

| Schedule Type | Example | Use Case |
|--------------|---------|----------|
| Daily at time | `every().day.at("08:00")` | Morning plan |
| Weekday at time | `every().monday.at("09:00")` | Weekly review |
| Weekly | `every().friday.at("15:00")` | Stakeholder discovery |
| Interval | `every(2).hours` | Periodic check |
| Immediate | `run_pending()` | Manual trigger |

---

## Security Architecture

### Secrets Management

```
.env (Local Development)
├── API Keys (encrypted at rest)
├── Tokens (never committed to git)
├── Google credentials path
└── Personal data

Production (Future)
├── AWS Secrets Manager
├── Environment variables
└── Encrypted config files
```

### Access Control

```
Google Workspace Scopes:
├── drive (File access)
├── documents (Doc read/write)
├── spreadsheets (Sheet read/write)
├── presentations (Slides read/write)
├── calendar (Event read/write)
└── tasks (Task management)

API Permissions:
├── AI: Read-only (no training on data)
└── Google: Limited to specified resources
```

---

## State Management

### Current State (Hybrid)

```
Each workflow can be:
- Stateless (fresh context each run)
- Cached (in-memory during session)
- Persisted (to Google Sheets/Drive)

Stakeholder data storage:
├── Profiles → Google Sheets
├── Reports → Google Docs
└── Tasks → Google Tasks
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

## Deployment Options

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

## Configuration Flow

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

## Testing Strategy

### Unit Tests (Future)
```python
tests/
├── test_execution_agent.py
├── test_stakeholder_discovery_agent.py
├── test_ai_client.py
├── test_google_clients.py
├── test_skills.py
└── test_config.py
```

### Integration Tests (Future)
```python
# Test full workflow
def test_stakeholder_discovery_workflow():
    # Mock Google APIs
    # Run workflow
    # Verify report generated
```

### Manual Testing (Current)
```bash
# Test each component
python config.py
python utils/ai_client.py
python utils/google/drive_client.py
python agents/stakeholder_discovery_agent.py
```

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

### Error Categories

| Level | Action | Example |
|-------|--------|---------|
| DEBUG | Log only | Verbose info |
| INFO | Log only | Workflow started |
| WARNING | Log + continue | API slow |
| ERROR | Log + alert | API failed |
| CRITICAL | Log + alert + halt | Config invalid |

---

## Future Enhancements

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

## Success Metrics

### System Health
- Uptime: Target 99%
- Workflow success rate: Target 95%
- Response time: Target < 30s

### User Value
- Time saved: Target 30%+
- Task completion: Target 85%+
- User satisfaction: Target 4.5/5

---

## Contributing

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
