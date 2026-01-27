# Personal OS for Product Management

> Automate your product management workflows with AI-powered agents that help you plan, execute, and communicate more effectively.

---

## 🚀 Quick Start

### **Start here:**

1. **[Claude CLI Commands](./.claude/commands/)** ⭐ - Run agents directly via `/command` in your Claude desktop app.
2. **[QUICK_START.md](./QUICK_START.md)** - Setup guide for full Python automation (Slack/Notion integration).

---

## 📦 What's Inside

### ✅ **Claude CLI Integration**

- Use `/daily-plan`, `/daily-summary`, `/discovery`, and more directly in your chat.
- Pre-configured for Product Management workflows.

### ✅ **Python Automation System** (Optional)

- 📋 Daily plan at 8:00 AM
- 📊 Progress check at 12:30 PM
- 🌟 Daily summary at 5:30 PM
- All delivered to Slack automatically!

---

## 🎯 Two Ways to Use This

### Option 1: Claude CLI Mode (Instant)

Use the powered-up commands directly in your Claude Desktop app.

- No complex setup required.
- Human-in-the-loop control.
- **Start here:** [./.claude/commands/](./.claude/commands/)

### Option 2: Full Automation (30 minutes)

Set up automated background workflows that run on schedule and push to Slack/Notion.

- Hands-free operation.
- Multi-tool integration.
- **Start here:** [QUICK_START.md](./QUICK_START.md)

---

## 📁 File Structure

```
Personal-OS/
├── README.md (this file)
├── QUICK_START.md          # Automation setup guide
├── personal-os-design.md   # System design & architecture
│
├── .claude/                # Claude Desktop Integration
│   └── commands/           # Slash commands (/daily-plan, etc.)
│
└── automation/             # Python automation engine
    ├── main.py
    ├── config.py
    └── requirements.txt
```

---

## 🚀 How to Execute Workflows

### Via Claude CLI (Recommended)

Simply type the slash command in your Claude chat:

- `/daily-plan` - Plan your day
- `/daily-summary` - Wrap up and prepare for tomorrow
- `/discovery` - Analyze user feedback
- `/strategy-check` - Align with OKRs

### Via Python Automation

1. Navigate to the automation folder: `cd automation`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your API keys in `.env`
4. Run: `python main.py`

---

**Built with ❤️ for Product Managers who want to focus on building great products, not managing tasks.**
