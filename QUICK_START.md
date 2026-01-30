# Personal OS - Complete Quick Start Guide

Get your Personal OS running in 30 minutes! 🚀

---

## 📦 What You've Built

A complete automation system with:

✅ **4 AI Agent Templates** - Ready-to-use prompts for Strategy, Discovery, Execution, and Stakeholder management
✅ **Python Automation Scripts** - Automated workflows that run on schedule
✅ **Slack Integration** - All updates delivered to your Slack DMs
✅ **AI-Powered** - Uses Claude or ChatGPT to generate plans and insights
✅ **Customizable** - Easy to adapt to your needs

---

## 🎯 Choose Your Path

### Path A: Start with Manual Mode (Recommended)
**Time**: 10 minutes
**Good for**: Testing the agents before automating

Jump to: [Manual Mode Setup](#manual-mode-setup)

### Path B: Full Automation
**Time**: 30 minutes
**Good for**: Running 24/7 automated workflows

Jump to: [Automation Setup](#automation-setup)

---

## Manual Mode Setup

### Step 1: Get an AI API Key

**Option A: Claude (Recommended)**
1. Go to https://console.anthropic.com/
2. Sign up and create an API key
3. Copy the key (starts with `sk-ant-`)

**Option B: ChatGPT**
1. Go to https://platform.openai.com/
2. Sign up and create an API key
3. Copy the key (starts with `sk-`)

### Step 2: Test an Agent

1. Open `agents/execution-agent.md`
2. Copy the "Daily Plan Generator" prompt (around line 30)
3. Go to Claude.ai or ChatGPT
4. Paste this prompt template:

```
ROLE: Personal Chief of Staff
CONTEXT: Planning your optimal workday for maximum impact

TODAY'S DATE: 2026-01-01 (Wednesday)

CALENDAR EVENTS:
- 9:30 AM: Team Standup (15 min)
- 2:00 PM: Product Review (1 hour)

OPEN TASKS:
- [High] Finish PRD for Feature X - Due: Friday - Est: 4 hours
- [High] Review design mocks - Due: Today - Est: 1 hour
- [Medium] Respond to customer feedback - Due: This week - Est: 30 min

STRATEGIC PRIORITIES:
- User activation
- Product quality
- Team efficiency

TASK:
Create a detailed daily execution plan following this format:
[Rest of prompt from template...]
```

4. Fill in YOUR actual calendar and tasks
5. Hit send and see your personalized daily plan!

**You can now use any agent template this way manually. No setup required!**

---

## Automation Setup

Follow these steps to get fully automated workflows running.

### Prerequisites Checklist

Before starting, make sure you have:
- [ ] Windows, Mac, or Linux computer
- [ ] Python 3.9+ installed ([Download here](https://www.python.org/downloads/))
- [ ] Slack workspace (free tier works fine)
- [ ] AI API key (Claude or OpenAI)
- [ ] 30 minutes of time

---

### Step 1: Install Python (if needed)

**Check if you have Python:**
```bash
python --version
# or
python3 --version
```

If you see version 3.9 or higher, you're good! Skip to Step 2.

**If not installed:**
- Windows/Mac: Download from https://www.python.org/downloads/
- Mac with Homebrew: `brew install python3`
- Linux: `sudo apt-get install python3` or `sudo yum install python3`

---

### Step 2: Open Terminal in Automation Folder

**Windows:**
1. Open File Explorer
2. Navigate to `C:\Users\RICHIE\Documents\personal_os\automation`
3. Click in the address bar and type `cmd`, press Enter

**Mac/Linux:**
```bash
cd ~/Documents/personal_os/automation
```

---

### Step 3: Install Dependencies

Run these commands:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

**Expected output**: Lots of downloading messages, ending with "Successfully installed..."

---

### Step 4: Create Slack Bot

#### 4.1 Create the App

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name: `Personal OS Bot`
4. Select your workspace
5. Click **"Create App"**

#### 4.2 Add Permissions

1. Click **"OAuth & Permissions"** in sidebar
2. Scroll to **"Bot Token Scopes"**
3. Click **"Add an OAuth Scope"** and add these:
   - `chat:write`
   - `users:read`
   - `channels:read`
   - `im:write`

#### 4.3 Install to Workspace

1. Scroll up to **"OAuth Tokens"**
2. Click **"Install to Workspace"**
3. Click **"Allow"**
4. **COPY THE TOKEN** (starts with `xoxb-`)
   - Save this somewhere - you'll need it in Step 5

#### 4.4 Get Your User ID

1. In Slack, click your profile picture
2. Click **"Profile"**
3. Click **⋯ (three dots)** → **"Copy member ID"**
   - Save this - you'll need it in Step 5

---

### Step 5: Configure Environment

1. In the `automation` folder, find `.env.example`
2. Copy it to create `.env`:
   ```bash
   # Windows
   copy .env.example .env

   # Mac/Linux
   cp .env.example .env
   ```

3. Open `.env` in any text editor (Notepad, VS Code, etc.)

4. Fill in these REQUIRED fields:

```bash
# === AI Configuration ===
# Paste your Claude API key here (from Step 1)
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here

# Which AI to use
AI_PROVIDER=anthropic

# === Slack Configuration ===
# Paste your Slack bot token here (from Step 4.3)
SLACK_BOT_TOKEN=xoxb-your-actual-token-here

# Paste your Slack user ID here (from Step 4.4)
SLACK_USER_ID=U01234567

# === Personal Info ===
USER_NAME=Your Name
USER_ROLE=Product Manager
COMPANY_NAME=Your Company

# Your main goals (comma-separated)
STRATEGIC_PRIORITIES=User activation, Product quality, Team efficiency

# === Settings ===
# Start with dry run mode to test
DRY_RUN=true
```

5. **Save the file**

---

### Step 6: Test Configuration

Run this command:

```bash
python config.py
```

**Expected output:**
```
Personal OS Configuration
==================================================
AI Provider: anthropic
AI Model: claude-sonnet-4-5-20250929
Task System: notion
Timezone: America/New_York
User: Your Name (Product Manager)
Dry Run: True

Enabled Agents:
  - Execution: True
  - Strategy: True
  - Discovery: True
  - Stakeholder: True

==================================================
✅ Configuration validated successfully
```

**If you see errors:**
- Check your API key is correct
- Check Slack token starts with `xoxb-`
- Check Slack user ID starts with `U`

---

### Step 7: Test Slack Connection

Run this command:

```bash
cd utils
python slack_client.py
```

**Expected outcome:** You should receive a test message in Slack!

**If nothing happens:**
1. Make sure `DRY_RUN=false` in `.env` (for testing)
2. Check your Slack bot token
3. Make sure the bot is installed in your workspace

---

### Step 8: Test AI Client

Run this command:

```bash
cd utils
python ai_client.py
```

**Expected outcome:** You should see a generated daily plan in your terminal

**If it fails:**
- Check your AI API key
- Make sure you have credits/quota available

---

### Step 9: Test Execution Agent

Run this command:

```bash
cd ..
cd agents
python execution_agent.py
```

**Expected outcome:** A fully generated daily plan in your terminal

**This is what will be sent to Slack every morning!**

---

### Step 10: Run Personal OS (Test Mode)

First, let's run in **DRY RUN** mode (no actual messages):

1. Make sure `.env` has:
   ```bash
   DRY_RUN=true
   ```

2. From the `automation` folder, run:
   ```bash
   # On Windows, you can double-click:
   run.bat

   # Or from command line:
   python main.py
   ```

**Expected output:**
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

3. Check `logs/personal_os.log` - you should see scheduled jobs logged

4. Press `Ctrl+C` to stop

---

### Step 11: Go Live!

Now let's run for real:

1. Edit `.env` and change:
   ```bash
   DRY_RUN=false
   ```

2. Run again:
   ```bash
   python main.py
   # or double-click run.bat on Windows
   ```

3. **You should get a startup message in Slack!**

```
🚀 Personal OS Started

Enabled agents:
✅ Execution Agent
✅ Strategy Agent
✅ Discovery Agent
✅ Stakeholder Agent

Next scheduled run: 2026-01-02 08:00:00
```

4. **Keep it running!** Your system will now:
   - Send daily plan at 8:00 AM
   - Send progress check at 12:30 PM
   - Send daily summary at 5:30 PM

---

## 🎉 You're Done!

Your Personal OS is now running. Here's what happens next:

### Tomorrow Morning (8:00 AM)
You'll receive a message like:
```
📋 Your Daily Plan

## Daily Execution Plan - 2026-01-02

### Top 3 Priorities:
1. Complete PRD for Feature X - Links to Q1 OKR - 4h
2. Review design mockups - Unblocks designer - 1h
3. Team standup preparation - 15m

### Time-Blocked Schedule:
8:00-9:00 AM: [FOCUS] PRD Writing
9:00-9:15 AM: Team Standup
...
```

---

## ⚙️ Customization

### Change Schedule Times

Edit `.env`:
```bash
# Change to 9 AM instead of 8 AM
EXECUTION_AGENT_MORNING_TIME=09:00

# Change to 1 PM instead of 12:30 PM
EXECUTION_AGENT_MIDDAY_TIME=13:00

# Change to 6 PM instead of 5:30 PM
EXECUTION_AGENT_EVENING_TIME=18:00
```

Restart the script to apply changes.

### Change Timezone

Edit `.env`:
```bash
# For Pacific Time
TIMEZONE=America/Los_Angeles

# For Central Time
TIMEZONE=America/Chicago

# For Eastern Time
TIMEZONE=America/New_York

# For London
TIMEZONE=Europe/London
```

### Disable Certain Workflows

Edit `.env`:
```bash
# Only run execution agent
ENABLE_EXECUTION_AGENT=true
ENABLE_STRATEGY_AGENT=false
ENABLE_DISCOVERY_AGENT=false
ENABLE_STAKEHOLDER_AGENT=false
```

### Customize Agent Prompts

1. Open `automation/agents/execution_agent.py`
2. Find the prompt you want to customize (around line 40)
3. Edit the prompt text
4. Save and restart the script

---

## 🔧 Troubleshooting

### Problem: "Module not found"
**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Problem: No Slack messages
**Solution:**
1. Check `DRY_RUN=false` in `.env`
2. Check Slack bot token is correct
3. Check bot is installed to workspace
4. Check `logs/personal_os.log` for errors

### Problem: "Configuration validation failed"
**Solution:**
- Open `.env` file
- Check all required fields are filled
- Check no typos in keys/tokens
- Run `python config.py` to see specific errors

### Problem: "AI API error"
**Solution:**
- Check your API key is valid
- Check you have credits/quota remaining
- Check the model name is correct

---

## 📱 Running 24/7

### Option 1: Keep Your Computer On
Simplest option - just leave the script running and your computer on.

**Pros:** Free, simple
**Cons:** Computer must stay on

### Option 2: Cloud Server ($5-10/month)
Deploy to a cloud server that runs 24/7:

**DigitalOcean/AWS/Linode:**
1. Create a small droplet/instance ($5-10/month)
2. Install Python
3. Copy your code to the server
4. Run as a background service

See `SETUP_GUIDE.md` for detailed cloud deployment instructions.

### Option 3: Run on Schedule
Use your computer's task scheduler:

**Windows Task Scheduler:**
- Create task that runs `run.bat` at startup
- Configure to run whether user is logged in or not

**Mac/Linux Cron:**
```bash
@reboot cd /path/to/automation && ./run.sh
```

---

## 📚 Next Steps

### Week 1: Learn the System
- [ ] Receive your first daily plan
- [ ] Review the outputs
- [ ] Adjust schedule times if needed
- [ ] Read through agent templates

### Week 2: Customize
- [ ] Edit agent prompts to match your style
- [ ] Add your actual calendar integration
- [ ] Connect to your task management system
- [ ] Fine-tune strategic priorities

### Week 3: Expand
- [ ] Try the other agent templates manually
- [ ] Build custom workflows
- [ ] Share with your team
- [ ] Measure time savings

---

## 📖 Documentation Reference

| Document | What It Covers |
|----------|---------------|
| `SETUP_GUIDE.md` | Detailed setup instructions |
| `README.md` | System overview and features |
| `ARCHITECTURE.md` | How everything works |
| `automation/AUTOMATION_README.md` | Python automation details |
| Individual agent files | Specific agent prompts |

---

## 🆘 Need Help?

1. Check `logs/personal_os.log` for errors
2. Review the troubleshooting section above
3. Read `SETUP_GUIDE.md` for detailed instructions
4. Test components individually

---

## 🎯 Success Checklist

You'll know it's working when:

- [x] Configuration validation passes
- [x] Slack test message received
- [x] AI client generates sample output
- [x] Execution agent test works
- [x] Startup message in Slack
- [x] First daily plan received

---

## 💡 Pro Tips

1. **Start with dry run mode** - Test everything before going live
2. **Check logs regularly** - `logs/personal_os.log` shows what's happening
3. **Customize gradually** - Start simple, add complexity over time
4. **Keep computer on** - Or deploy to cloud for 24/7 operation
5. **Review outputs** - Fine-tune prompts based on what you receive
6. **Share wins** - Show your team how much time you're saving

---

## 🎊 Congratulations!

You now have a fully automated Personal OS that will:

✅ Plan your day every morning
✅ Check your progress at midday
✅ Summarize your achievements every evening
✅ Keep you aligned with strategic goals
✅ Save you 30%+ time on planning and updates

**Welcome to the future of productivity!** 🚀

---

**Questions? Review the documentation files or check the logs for debugging.**
