# Personal OS Automation - Setup Guide

This guide will walk you through setting up your Personal OS automation system step-by-step.

---

## Prerequisites

Before you begin, you'll need:

1. **Python 3.9 or higher** installed
2. **Google account** with access to Google Workspace (Drive, Docs, Calendar, etc.)
3. **AI API key** (Anthropic Claude or OpenAI)
4. Basic command line knowledge

Optional (for full integration):
- Task management tool account (Notion, Jira, etc.)

---

## Step-by-Step Setup

### Step 1: Install Python Dependencies

Open a terminal in the `automation` directory and run:

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Expected output**: All packages installed successfully

---

### Step 2: Set Up Google Cloud Project

#### 2.1 Create a Project

1. Go to https://console.cloud.google.com/
2. Click **"Select a project"** dropdown at the top
3. Click **"New Project"**
4. Project name: `Personal OS`
5. Click **"Create"**
6. Wait for the project to be created

#### 2.2 Enable APIs

1. Make sure your new project is selected
2. Go to **"APIs & Services"** > **"Enable APIs and Services"**
3. Search for and enable each of these APIs:
   - **Google Drive API** - Click "Enable"
   - **Google Docs API** - Click "Enable"
   - **Google Sheets API** - Click "Enable"
   - **Google Slides API** - Click "Enable"
   - **Google Calendar API** - Click "Enable"
   - **Tasks API** - Click "Enable"

#### 2.3 Configure OAuth Consent Screen

1. Go to **"APIs & Services"** > **"OAuth consent screen"**
2. Choose **"External"** (or "Internal" if using Google Workspace)
3. Click **"Create"**
4. Fill in:
   - App name: `Personal OS`
   - User support email: Your email
   - Developer contact: Your email
5. Click **"Save and Continue"**
6. On Scopes page, click **"Add or Remove Scopes"**
7. Add these scopes:
   - `https://www.googleapis.com/auth/drive`
   - `https://www.googleapis.com/auth/documents`
   - `https://www.googleapis.com/auth/spreadsheets`
   - `https://www.googleapis.com/auth/presentations`
   - `https://www.googleapis.com/auth/calendar`
   - `https://www.googleapis.com/auth/tasks`
8. Click **"Update"** then **"Save and Continue"**
9. Add your email as a test user
10. Click **"Save and Continue"**

#### 2.4 Create OAuth Credentials

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** > **"OAuth client ID"**
3. Application type: **"Desktop app"**
4. Name: `Personal OS Desktop`
5. Click **"Create"**
6. Click **"Download JSON"**
7. Save the file as `credentials/google_credentials.json` in your automation directory

```bash
# Create credentials directory
mkdir -p credentials

# Move your downloaded file
mv ~/Downloads/client_secret_*.json credentials/google_credentials.json
```

---

### Step 3: Get AI API Key

#### Option A: Anthropic Claude (Recommended)

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Go to **"API Keys"**
4. Click **"Create Key"**
5. **Copy your API key** (starts with `sk-ant-`)
   - Save this - you'll need it next

#### Option B: OpenAI GPT

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Go to **"API Keys"**
4. Click **"Create new secret key"**
5. **Copy your API key** (starts with `sk-`)
   - Save this - you'll need it next

---

### Step 4: Configure Environment Variables

1. In the `automation` directory, find `.env.example`
2. **Copy it** and rename to `.env`:
   ```bash
   cp .env.example .env
   ```

3. **Edit `.env`** with your favorite text editor
4. Fill in the following **required** values:

```bash
# AI Provider (choose one)
ANTHROPIC_API_KEY=sk-ant-your-key-here
# OR
OPENAI_API_KEY=sk-your-key-here

# Which provider to use
AI_PROVIDER=anthropic  # or "openai"

# Google Workspace Configuration
GOOGLE_CREDENTIALS_FILE=credentials/google_credentials.json
GOOGLE_CALENDAR_ID=primary  # or your-email@gmail.com

# Optional: Specify a folder for stakeholder documents
# GOOGLE_DRIVE_FOLDER_ID=your-folder-id

# Personal Context
USER_NAME=Your Name
USER_ROLE=Product Manager
COMPANY_NAME=Your Company

# Strategic Priorities (comma-separated)
STRATEGIC_PRIORITIES=User activation, Product quality, Team efficiency
```

5. **Save the file**

---

### Step 5: Test Your Configuration

Run the configuration test:

```bash
python config.py
```

**Expected output**:
```
Personal OS Configuration
==================================================
AI Provider: anthropic
AI Model: claude-sonnet-4-5-20250929
Task System: google_tasks
Timezone: America/New_York
User: Your Name (Product Manager)
Dry Run: False

Enabled Agents:
  - Execution: True
  - Strategy: True
  - Discovery: True
  - Stakeholder: True

==================================================
Configuration validated successfully
```

If you see errors, double-check your `.env` file.

---

### Step 6: Authenticate with Google

The first time you run Personal OS, it will open a browser for Google authentication:

```bash
python main.py
```

1. A browser window will open
2. Select your Google account
3. You may see a warning: "This app isn't verified" - click **"Advanced"** > **"Go to Personal OS"**
4. Review permissions and click **"Allow"**
5. Close the browser tab when prompted
6. A token file will be saved to `credentials/token.json`

**Expected output**: Personal OS starts running

---

### Step 7: Test AI Client

Run the AI client test:

```bash
cd utils
python ai_client.py
```

**Expected output**: A generated daily plan example

If this fails, check your AI API key.

---

### Step 8: Test Google Integration

Test the Google clients:

```bash
# Test Drive search
python -c "from utils.google import GoogleDriveClient; c = GoogleDriveClient(); print('Drive OK')"

# Test Calendar
python -c "from utils.google import GoogleCalendarClient; c = GoogleCalendarClient(); print(c.get_todays_events())"
```

**Expected output**: Empty list or your today's events

---

### Step 9: Test Stakeholder Discovery Agent

Run the stakeholder discovery agent:

```bash
python agents/stakeholder_discovery_agent.py
```

**Expected output**: Agent searches for documents and generates a report

---

### Step 10: Run Personal OS (Dry Run Mode)

First, let's run in dry run mode (won't create actual documents):

1. Edit `.env` and set:
   ```bash
   DRY_RUN=true
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

**Expected output**:
```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║              PERSONAL OS - AUTOMATION SYSTEM                  ║
║                                                               ║
║   Automating your product management workflows                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Personal OS is now running...
Press Ctrl+C to stop
```

3. Check the logs:
   - Look in `logs/personal_os.log`
   - You should see scheduled jobs logged

4. Press `Ctrl+C` to stop

---

### Step 11: Run Personal OS (Live Mode)

Once you're confident everything works:

1. Edit `.env` and set:
   ```bash
   DRY_RUN=false
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

3. **Let it run!** The system will:
   - Generate daily plan at 8:00 AM (saved to Google Docs)
   - Check progress at 12:30 PM
   - Summarize your day at 5:30 PM
   - Run stakeholder discovery on Fridays

---

## Scheduled Workflows

Your Personal OS will now run these workflows automatically:

### Daily Workflows

| Time | Workflow | What It Does |
|------|----------|--------------|
| 8:00 AM | Morning Daily Plan | Generates your prioritized plan for the day |
| 12:30 PM | Midday Progress Check | Checks progress and suggests adjustments |
| 5:30 PM | Evening Summary | Summarizes achievements and preps tomorrow |

### Weekly Workflows

| When | Workflow | What It Does |
|------|----------|--------------|
| Friday 3:00 PM | Stakeholder Discovery | Analyzes meeting notes and builds stakeholder profiles |

---

## Customization

### Change Schedule Times

Edit `.env`:
```bash
EXECUTION_AGENT_MORNING_TIME=09:00  # Change to 9 AM
EXECUTION_AGENT_MIDDAY_TIME=13:00   # Change to 1 PM
EXECUTION_AGENT_EVENING_TIME=18:00  # Change to 6 PM
```

### Enable/Disable Agents

Edit `.env`:
```bash
ENABLE_EXECUTION_AGENT=true
ENABLE_STRATEGY_AGENT=false  # Disable strategy agent
ENABLE_DISCOVERY_AGENT=true
ENABLE_STAKEHOLDER_AGENT=true
```

### Change Your Timezone

Edit `.env`:
```bash
TIMEZONE=America/Los_Angeles  # PST
# Other examples:
# America/New_York (EST)
# Europe/London (GMT)
# Asia/Tokyo (JST)
```

---

## Advanced: Task Management Integration

### Option A: Notion Integration

1. Get your Notion API key:
   - Go to https://www.notion.so/my-integrations
   - Click **"Create new integration"**
   - Copy the **Internal Integration Token**

2. Get your database ID:
   - Open your tasks database in Notion
   - Click **"Share"** → **"Invite"** → Add your integration
   - Copy the database ID from the URL:
     `https://notion.so/your-workspace/DATABASE_ID?v=...`

3. Edit `.env`:
   ```bash
   TASK_SYSTEM=notion
   NOTION_API_KEY=secret_your_key_here
   NOTION_DATABASE_ID=your_database_id_here
   ```

### Option B: Jira Integration

1. Get API token:
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click **"Create API token"**

2. Edit `.env`:
   ```bash
   TASK_SYSTEM=jira
   JIRA_URL=https://your-domain.atlassian.net
   JIRA_EMAIL=your-email@company.com
   JIRA_API_TOKEN=your_token_here
   JIRA_PROJECT_KEY=PROJ
   ```

---

## Troubleshooting

### Problem: "Configuration validation failed"

**Solution**: Check your `.env` file. Make sure:
- AI API key is correct
- Google credentials file exists at the configured path

### Problem: "Google API error: invalid credentials"

**Solution**:
1. Delete `credentials/token.json`
2. Run `python main.py` again
3. Complete the OAuth flow in your browser

### Problem: "Access Denied" from Google

**Solution**:
1. Make sure you added your email as a test user in OAuth consent screen
2. Verify all APIs are enabled
3. Check the credentials file is valid JSON

### Problem: "Module not found"

**Solution**: Make sure you activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Problem: No reports generated

**Solution**:
1. Check if `DRY_RUN=false` in `.env`
2. Check logs in `logs/personal_os.log`
3. Verify Google credentials are working

---

## Next Steps

### Week 1: Getting Started
1. Complete this setup
2. Run your first stakeholder discovery
3. Review the generated report
4. Adjust schedule times if needed

### Week 2: Customize
1. Fine-tune your strategic priorities
2. Customize agent prompts (in `agents/` files)
3. Add more documents to your Drive folder
4. Review stakeholder profiles

### Week 3: Expand
1. Enable other agents (Strategy, Discovery)
2. Add custom workflows
3. Integrate with Notion/Jira
4. Share insights with team

### Month 2: Advanced
1. Build custom agents
2. Add metrics tracking
3. Create dashboards
4. Automate more workflows

---

## Additional Resources

### File Structure
```
automation/
├── main.py                 # Main runner
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env                   # Your secrets (don't commit!)
├── .env.example          # Template
├── credentials/          # Google credentials (don't commit!)
│   ├── google_credentials.json
│   └── token.json
├── agents/
│   ├── execution_agent.py
│   └── stakeholder_discovery_agent.py
├── skills/               # Reusable skills
├── models/               # Data models
├── utils/
│   ├── ai_client.py
│   └── google/          # Google Workspace clients
└── logs/
    └── personal_os.log    # Application logs
```

### Useful Commands

```bash
# Start Personal OS
python main.py

# Test configuration
python config.py

# Test specific agent
python agents/execution_agent.py
python agents/stakeholder_discovery_agent.py

# View logs (live)
tail -f logs/personal_os.log

# Stop Personal OS
Ctrl+C
```

---

## Getting Help

If you run into issues:

1. Check the logs: `logs/personal_os.log`
2. Run in dry run mode to debug
3. Test components individually
4. Review this guide again

---

## Success!

Once everything is working, you'll see reports generated in Google Docs and tasks created in Google Tasks. Your Personal OS is now running and will help you stay organized and productive every day!

---

**Pro Tip**: Keep the automation running 24/7 by deploying to a server (AWS, DigitalOcean, etc.) or running it on a spare computer/Raspberry Pi.
