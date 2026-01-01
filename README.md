# Personal OS for Product Management

> Automate your product management workflows with AI-powered agents that help you plan, execute, and communicate more effectively.

---

## 🚀 Quick Start

### **New here? Start with one of these:**

1. **[QUICK_START.md](./QUICK_START.md)** ⭐ - 30-minute setup guide for automation
2. **[INDEX.md](./INDEX.md)** - Complete navigation and documentation hub
3. **[agents/README.md](./agents/README.md)** - Use agent templates manually (no setup)

---

## 📦 What's Inside

### ✅ **4 AI Agent Templates** with 20+ ready-to-use prompts
- **Strategy Agent** - OKR planning, competitive analysis, strategic alignment
- **Discovery Agent** - User interviews, feedback analysis, feature requests
- **Execution Agent** - Daily planning, progress tracking, summaries
- **Stakeholder Agent** - Meeting prep, status updates, communication

### ✅ **Python Automation System** that runs 24/7
- 📋 Daily plan at 8:00 AM
- 📊 Progress check at 12:30 PM
- 🌟 Daily summary at 5:30 PM
- All delivered to Slack automatically!

### ✅ **Complete Documentation**
- Setup guides, architecture docs, troubleshooting, and more

---

## 🎯 Two Ways to Use This

### Option 1: Manual Mode (5 minutes)
Copy any prompt from the agent templates and use with ChatGPT or Claude.
- No setup required
- Start immediately
- Perfect for testing

**Start here:** [agents/README.md](./agents/README.md)

### Option 2: Full Automation (30 minutes)
Set up automated workflows that run on schedule.
- Daily automated updates
- Hands-free operation
- Maximum productivity

**Start here:** [QUICK_START.md](./QUICK_START.md)

---

## 📁 File Structure

```
Productivity/
├── README.md (this file)
├── QUICK_START.md          # 30-min automation setup
├── INDEX.md                # Complete navigation
├── personal-os-design.md   # System design
│
├── agents/                 # Agent templates (manual)
│   ├── strategy-agent.md
│   ├── discovery-agent.md
│   ├── execution-agent.md
│   └── stakeholder-agent.md
│
└── automation/             # Python automation
    ├── main.py
    ├── config.py
    ├── requirements.txt
    └── ... (full system)
```

---

## 🎉 Get Started Now

1. **Explore:** Open [INDEX.md](./INDEX.md) for complete documentation
2. **Quick test:** Try a manual prompt from [agents/README.md](./agents/README.md)
3. **Full setup:** Follow [QUICK_START.md](./QUICK_START.md) for automation

---

## 🚀 How to Start & Execute Workflows

### Quick Start (5 minutes)
1. Navigate to the automation folder:
   ```bash
   cd automation
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   # Copy template
   cp .env.example .env

   # Edit .env with your API keys
   # Required: ANTHROPIC_API_KEY, SLACK_BOT_TOKEN, SLACK_USER_ID
   ```

4. Run the system:
   ```bash
   # Test mode (no actual messages)
   python main.py

   # Or on Windows, double-click:
   run.bat
   ```

### Executing Workflows

**Option 1: Automated (Default)**
The system runs automatically based on schedule:
- 8:00 AM - Daily plan
- 12:30 PM - Progress check
- 5:30 PM - Daily summary

Just keep `python main.py` running in the background.

**Option 2: Manual Execution**
Run individual agents on-demand:
```bash
# Execute daily planning workflow
python automation/agents/execution_agent.py

# Test individual components
python automation/utils/ai_client.py
python automation/utils/slack_client.py
```

**Option 3: Custom Schedule**
Edit `.env` to customize timing:
```bash
EXECUTION_AGENT_MORNING_TIME=09:00
EXECUTION_AGENT_MIDDAY_TIME=13:00
EXECUTION_AGENT_EVENING_TIME=18:00
```

For detailed instructions, see [QUICK_START.md](./QUICK_START.md)

---

**Built with ❤️ for Product Managers who want to focus on building great products, not managing tasks.**
