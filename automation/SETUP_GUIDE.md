# Personal OS Automation - Setup Guide

This guide will walk you through setting up your Personal OS automation system step-by-step.

---

## 📋 Prerequisites

Before you begin, you'll need:

1. **Python 3.9 or higher** installed
2. **Slack workspace** with admin access (to create bot)
3. **AI API key** (Anthropic Claude or OpenAI)
4. Basic command line knowledge

Optional (for full integration):
- Google Calendar account
- Task management tool account (Notion, Jira, etc.)

---

## 🚀 Step-by-Step Setup

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

### Step 2: Set Up Slack Bot

#### 2.1 Create a Slack App

1. Go to https://api.slack.com/apps
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. App Name: `Personal OS Bot`
5. Workspace: Select your workspace
6. Click **"Create App"**

#### 2.2 Configure Bot Permissions

1. In your app settings, go to **"OAuth & Permissions"**
2. Scroll to **"Scopes"** → **"Bot Token Scopes"**
3. Add these scopes:
   - `chat:write` - Send messages
   - `users:read` - Read user information
   - `channels:read` - List channels
   - `im:write` - Send DMs

4. Scroll up and click **"Install to Workspace"**
5. Click **"Allow"**
6. **Copy the Bot User OAuth Token** (starts with `xoxb-`)
   - Save this - you'll need it in Step 3

#### 2.3 Get Your Slack User ID

1. In Slack, click your profile picture → **"Profile"**
2. Click the **⋯ (three dots)** → **"Copy member ID"**
   - Save this - you'll need it in Step 3

#### 2.4 Create a Channel (Optional)

1. In Slack, create a new channel: `#personal-os-updates`
2. Invite your bot: Type `/invite @Personal OS Bot` in the channel

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

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_USER_ID=U0123456789  # Your user ID from Step 2.3

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
Task System: notion
Timezone: America/New_York
User: Your Name (Product Manager)
Dry Run: False

Enabled Agents:
  - Execution: True
  - Strategy: True
  - Discovery: True
  - Stakeholder: True

==================================================
✅ Configuration validated successfully
```

If you see errors, double-check your `.env` file.

---

### Step 6: Test AI Client

Run the AI client test:

```bash
cd utils
python ai_client.py
```

**Expected output**: A generated daily plan example

If this fails, check your AI API key.

---

### Step 7: Test Slack Client

Run the Slack client test:

```bash
cd utils
python slack_client.py
```

**Expected output**: A test message in your Slack DMs

If you don't receive a message:
1. Check your Slack bot token
2. Make sure the bot is installed in your workspace
3. Verify your user ID is correct

---

### Step 8: Test Execution Agent

Run the execution agent test:

```bash
cd agents
python execution_agent.py
```

**Expected output**: A generated daily plan in your terminal

---

### Step 9: Run Personal OS (Dry Run Mode)

First, let's run in dry run mode (won't send actual messages):

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
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║              PERSONAL OS - AUTOMATION SYSTEM              ║
║                                                           ║
║   Automating your product management workflows           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

Personal OS is now running...
Press Ctrl+C to stop
```

3. Check the logs:
   - Look in `logs/personal_os.log`
   - You should see scheduled jobs logged

4. Press `Ctrl+C` to stop

---

### Step 10: Run Personal OS (Live Mode)

Once you're confident everything works:

1. Edit `.env` and set:
   ```bash
   DRY_RUN=false
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

3. You should receive a startup message in Slack!

4. **Let it run!** The system will:
   - Send daily plan at 8:00 AM
   - Send progress check at 12:30 PM
   - Send daily summary at 5:30 PM

---

## ⏰ Scheduled Workflows

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
| Friday 3:00 PM | Weekly Status Update | Generates status update for stakeholders |

---

## 🎨 Customization

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

### Change Slack Channels

Edit `.env`:
```bash
SLACK_CHANNEL_DAILY=#my-daily-updates
SLACK_CHANNEL_WEEKLY=#weekly-summaries
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

## 🔧 Advanced: Integrate with Task Management

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

## 📱 Advanced: Google Calendar Integration

1. Enable Google Calendar API:
   - Go to https://console.cloud.google.com/
   - Create a new project
   - Enable Google Calendar API
   - Create credentials (OAuth 2.0)
   - Download credentials JSON

2. Save credentials:
   ```bash
   mkdir credentials
   # Move your downloaded JSON file to:
   # credentials/google_calendar_credentials.json
   ```

3. Edit `.env`:
   ```bash
   GOOGLE_CALENDAR_CREDENTIALS=credentials/google_calendar_credentials.json
   GOOGLE_CALENDAR_ID=your-email@gmail.com
   ```

---

## 🐛 Troubleshooting

### Problem: "Configuration validation failed"

**Solution**: Check your `.env` file. Make sure:
- AI API key is correct
- Slack bot token starts with `xoxb-`
- Slack user ID starts with `U`

### Problem: "Slack API error: invalid_auth"

**Solution**: Your Slack bot token is invalid or expired
1. Go to https://api.slack.com/apps
2. Select your app
3. Go to "OAuth & Permissions"
4. Copy the Bot User OAuth Token again
5. Update `.env` file

### Problem: No messages received

**Solution**:
1. Check if bot is installed: Look for `@Personal OS Bot` in your workspace
2. Check DRY_RUN setting in `.env` (should be `false`)
3. Check logs in `logs/personal_os.log`

### Problem: "Module not found"

**Solution**: Make sure you activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

## 🎯 Next Steps

### Week 1: Getting Started
1. ✅ Complete this setup
2. ✅ Receive your first daily plan
3. ✅ Review and provide feedback (mental notes)
4. ✅ Adjust schedule times if needed

### Week 2: Customize
1. Fine-tune your strategic priorities
2. Customize agent prompts (in `agents/` files)
3. Add your actual tasks (integrate with task system)
4. Connect Google Calendar

### Week 3: Expand
1. Enable other agents (Strategy, Discovery)
2. Add custom workflows
3. Integrate with more tools
4. Share insights with team

### Month 2: Advanced
1. Build custom agents
2. Add metrics tracking
3. Create dashboards
4. Automate more workflows

---

## 📚 Additional Resources

### File Structure
```
automation/
├── main.py                 # Main runner
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env                   # Your secrets (don't commit!)
├── .env.example          # Template
├── agents/
│   └── execution_agent.py
├── utils/
│   ├── ai_client.py
│   └── slack_client.py
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

# View logs (live)
tail -f logs/personal_os.log

# Stop Personal OS
Ctrl+C
```

---

## 🆘 Getting Help

If you run into issues:

1. Check the logs: `logs/personal_os.log`
2. Run in dry run mode to debug
3. Test components individually
4. Review this guide again

---

## 🎉 Success!

Once you see this in Slack, you're all set:

```
🚀 Personal OS Started

Enabled agents:
✅ Execution Agent
✅ Strategy Agent
✅ Discovery Agent
✅ Stakeholder Agent

Next scheduled run: 2026-01-02 08:00:00
```

Your Personal OS is now running and will help you stay organized and productive every day!

---

**Pro Tip**: Keep the automation running 24/7 by deploying to a server (AWS, DigitalOcean, etc.) or running it on a spare computer/Raspberry Pi.
