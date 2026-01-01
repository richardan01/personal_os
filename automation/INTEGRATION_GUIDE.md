# Integration Guide - Messaging Platforms

Personal OS supports multiple messaging platforms. Choose the one that works best for you!

---

## 🎯 Supported Platforms

### ✅ Slack
The original integration - popular in Western companies.

**Setup Guide:** See main [SETUP_GUIDE.md](./SETUP_GUIDE.md)

**Best for:**
- English-speaking teams
- Western companies
- Integration with other Slack apps

---

### ✅ Lark (Feishu)
Full support for Lark/Feishu - popular in Asian markets.

**Setup Guide:** [LARK_SETUP.md](./LARK_SETUP.md)

**Best for:**
- Chinese teams
- Asian companies
- ByteDance ecosystem users

---

### ✅ Both!
Send updates to BOTH platforms simultaneously.

---

## 🚀 Quick Setup Comparison

| Step | Slack | Lark |
|------|-------|------|
| **Create App** | api.slack.com/apps | open.feishu.cn (or open.larksuite.com) |
| **Get Credentials** | Bot Token (xoxb-) | App ID (cli_) + Secret |
| **Get User ID** | Copy Member ID | Get open_id (ou_) |
| **Add to .env** | SLACK_BOT_TOKEN, SLACK_USER_ID | LARK_APP_ID, LARK_APP_SECRET, LARK_USER_ID |
| **Set Platform** | MESSAGING_PLATFORM=slack | MESSAGING_PLATFORM=lark |

---

## ⚙️ Configuration

### Option 1: Slack Only

```bash
# In .env file
MESSAGING_PLATFORM=slack

# Slack credentials
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_USER_ID=U01234567
```

### Option 2: Lark Only

```bash
# In .env file
MESSAGING_PLATFORM=lark

# Lark credentials
LARK_APP_ID=cli_your_app_id
LARK_APP_SECRET=your_secret
LARK_USER_ID=ou_your_open_id
```

### Option 3: Both Platforms

```bash
# In .env file
MESSAGING_PLATFORM=both

# Slack credentials
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_USER_ID=U01234567

# Lark credentials
LARK_APP_ID=cli_your_app_id
LARK_APP_SECRET=your_secret
LARK_USER_ID=ou_your_open_id
```

When set to `both`, you'll receive messages on BOTH platforms!

---

## 📱 Platform Features

### Slack Features
- Rich text formatting with Slack blocks
- Thread support
- Channel mentions
- File attachments
- Interactive buttons (coming soon)

### Lark Features
- Rich text cards
- Interactive elements
- Markdown support
- Group chat support
- File sharing

### Both Platforms
All core Personal OS features work on both:
- Daily plans
- Progress checks
- Daily summaries
- Status updates
- Alerts

---

## 🔧 Switching Platforms

You can change platforms anytime:

1. Edit `.env` file
2. Change `MESSAGING_PLATFORM` value
3. Restart Personal OS:
   ```bash
   python main.py
   ```

No code changes needed!

---

## 🧪 Testing

### Test Slack
```bash
cd utils
python slack_client.py
```

### Test Lark
```bash
cd utils
python lark_client.py
```

### Test Unified Client
```bash
cd utils
python messaging_client.py
```

---

## 📊 When to Use What

### Use Slack When:
- Your team is already on Slack
- You're in a Western company
- You want Slack app integrations
- English is primary language

### Use Lark When:
- Your team is on Lark/Feishu
- You're in an Asian company
- You want ByteDance ecosystem integration
- Chinese/Asian language support

### Use Both When:
- You use both platforms
- You want redundancy
- You're bridging teams on different platforms
- You want maximum visibility

---

## 🆘 Troubleshooting

### Messages Only Going to One Platform

**Check your .env:**
```bash
MESSAGING_PLATFORM=both  # Make sure it says "both"
```

**Check credentials:**
- Both platforms need valid credentials
- Test each platform independently first

### One Platform Working, Other Not

**Check logs:**
```bash
tail -f logs/personal_os.log
```

Look for error messages specific to the failing platform.

**Verify configuration:**
```bash
python config.py
```

Should show both platforms configured.

---

## 📚 Detailed Setup Guides

- **Slack Setup**: [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Steps 2-7
- **Lark Setup**: [LARK_SETUP.md](./LARK_SETUP.md) - Complete guide

---

## ✅ Configuration Checklist

### For Slack:
- [ ] Created Slack app
- [ ] Added required scopes (chat:write, users:read, etc.)
- [ ] Installed to workspace
- [ ] Copied Bot Token to .env
- [ ] Copied User ID to .env
- [ ] Test message received

### For Lark:
- [ ] Created Lark custom app
- [ ] Added required scopes (im:message, etc.)
- [ ] Published and installed app
- [ ] Copied App ID and Secret to .env
- [ ] Got Open ID and saved to .env
- [ ] Test message received

### For Both:
- [ ] MESSAGING_PLATFORM=both in .env
- [ ] All credentials configured
- [ ] Both tests successful
- [ ] Personal OS running
- [ ] Messages received on both platforms

---

## 🎉 Next Steps

Once configured:

1. **Run Personal OS:**
   ```bash
   python main.py
   ```

2. **Receive your first update** on your chosen platform(s)

3. **Enjoy automated productivity!**

---

**Pro Tip:** Start with one platform to test, then add the second platform once you're comfortable!
