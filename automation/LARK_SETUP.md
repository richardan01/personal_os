# Lark (Feishu) Integration Setup Guide

This guide will help you set up Lark integration for your Personal OS.

---

## 📋 Prerequisites

- Lark (Feishu) account with admin access
- Access to create custom apps in your Lark workspace

---

## 🚀 Step-by-Step Setup

### Step 1: Create a Lark Custom App

1. Go to [Lark Open Platform](https://open.larksuite.com/)
   - For Feishu (China): https://open.feishu.cn/
   - For Lark (International): https://open.larksuite.com/

2. Click **"Create custom app"**

3. Fill in app details:
   - **App Name**: `Personal OS Bot`
   - **Description**: `AI-powered productivity assistant`
   - **App Icon**: Upload an icon (optional)

4. Click **"Create"**

5. **Save your credentials**:
   - **App ID**: Starts with `cli_` (e.g., `cli_a1b2c3d4e5f6g7h8`)
   - **App Secret**: Copy the secret key

---

### Step 2: Configure App Permissions

1. In your app dashboard, go to **"Permissions & Scopes"**

2. Add the following **API scopes**:

#### Required Scopes:
- `im:message` - Send messages
- `im:message:send_as_bot` - Send as bot
- `contact:user.base:readonly` - Read user basic info
- `contact:user:readonly` - Read user details (optional)

3. Click **"Save"** and then **"Submit for Review"** (if required)

---

### Step 3: Enable Bot Features

1. Go to **"Features"** → **"Bot"**

2. Enable **Bot Capabilities**

3. Configure bot settings:
   - Bot name: `Personal OS`
   - Description: Brief description of what it does
   - Commands: (optional, can add later)

---

### Step 4: Get Your User Open ID

There are two ways to get your Lark user ID:

#### Method A: Using Bot (Easier)

1. After app approval, add the bot to a test group
2. Send a message to the bot
3. Use the [Message Debugger](https://open.feishu.cn/document/home/message-debugger) to see the `open_id`

#### Method B: Using API

1. Use this API endpoint:
   ```
   GET https://open.feishu.cn/open-apis/contact/v3/users/me
   ```

2. Or run this command (after setting up your app):
   ```bash
   cd automation
   python -c "from utils.lark_client import lark_client; print(lark_client.get_user_info())"
   ```

3. Your `open_id` will start with `ou_` (e.g., `ou_a1b2c3d4e5f6g7h8`)

---

### Step 5: Publish and Install App

1. Go to **"Version Management & Release"**

2. Click **"Create Version"**:
   - Version name: `v1.0`
   - Update description: `Initial release`

3. Click **"Submit for Release"**

4. Once approved, **install the app** to your workspace:
   - Go to **"Availability"**
   - Click **"Add to Workspace"**
   - Select your workspace
   - Confirm installation

---

### Step 6: Configure .env File

1. Open `C:\Users\RICHIE\Documents\Productivity\automation\.env`

2. Add your Lark credentials:

```bash
# Lark (Feishu) Integration
LARK_APP_ID=cli_your_actual_app_id_here
LARK_APP_SECRET=your_actual_app_secret_here
LARK_USER_ID=ou_your_actual_open_id_here

# Which messaging platform to use
MESSAGING_PLATFORM=lark  # or "both" for Slack + Lark
```

3. Save the file

---

### Step 7: Test Lark Integration

Run the test script:

```bash
cd automation
python utils/lark_client.py
```

**Expected output:**
```
Testing Lark Client...
==================================================
✅ Test message sent successfully
==================================================
```

You should receive a test message in Lark!

---

## 🎨 Messaging Platform Options

You can configure which platform(s) to use:

### Option 1: Lark Only
```bash
MESSAGING_PLATFORM=lark
```

### Option 2: Slack Only
```bash
MESSAGING_PLATFORM=slack
```

### Option 3: Both Platforms
```bash
MESSAGING_PLATFORM=both
```

When set to `both`, Personal OS will send messages to both Slack AND Lark simultaneously.

---

## 📱 Using Lark Features

### Send to a Specific Chat/Group

1. Get the chat ID:
   - Open the group chat in Lark
   - Click group settings → **More** → **Copy chat ID**
   - Chat ID starts with `oc_` (e.g., `oc_a1b2c3d4e5f6g7h8`)

2. Update `.env`:
   ```bash
   LARK_CHAT_ID=oc_your_chat_id_here
   ```

3. Modify the code to send to chat instead of DM (optional)

---

## 🔧 Troubleshooting

### Problem: "Invalid app credentials"

**Solution:**
- Double-check your App ID and App Secret in `.env`
- Make sure there are no extra spaces
- Verify the app is published and installed

### Problem: "Permission denied"

**Solution:**
- Check that you've added all required scopes
- Re-submit the app for approval if scopes changed
- Reinstall the app after permission changes

### Problem: No messages received

**Solution:**
1. Check `DRY_RUN=false` in `.env`
2. Verify your `LARK_USER_ID` is correct
3. Make sure bot is added to workspace
4. Check logs: `tail -f logs/personal_os.log`

### Problem: "Access token expired"

**Solution:**
- The system automatically refreshes tokens
- If issue persists, restart Personal OS:
  ```bash
  python main.py
  ```

---

## 🌐 Lark vs Feishu

### What's the Difference?

- **Feishu (飞书)**: Chinese version (feishu.cn)
- **Lark**: International version (larksuite.com)

### Which Endpoints to Use?

**If using Feishu (China):**
```python
# Already configured in lark_client.py
https://open.feishu.cn/open-apis/...
```

**If using Lark (International):**
Update `lark_client.py` and change:
```python
# Change from:
https://open.feishu.cn/open-apis/...

# To:
https://open.larksuite.com/open-apis/...
```

---

## 📊 Message Format Examples

### Plain Text
```python
messaging_client.send_dm("Hello from Personal OS!")
```

### Markdown
```python
messaging_client.send_dm("""
**Daily Plan**

Your top priorities:
1. Task A
2. Task B
3. Task C
""")
```

### Rich Cards (Advanced)
Lark supports interactive cards. See `lark_client.py` for examples of:
- `send_card()` - Interactive cards with buttons
- `send_rich_text()` - Formatted rich text
- `send_daily_plan()` - Pre-formatted daily plan card

---

## 🔐 Security Best Practices

1. **Never commit `.env`** - It's already in `.gitignore`

2. **Rotate credentials** periodically:
   - Go to Lark app dashboard
   - Generate new App Secret
   - Update `.env` file

3. **Use least privilege**:
   - Only request scopes you need
   - Review permissions quarterly

4. **Monitor usage**:
   - Check Lark app dashboard for API usage
   - Set up alerts for unusual activity

---

## 📚 Additional Resources

### Official Documentation
- [Lark Open Platform](https://open.larksuite.com/)
- [Feishu Open Platform](https://open.feishu.cn/)
- [Lark API Reference](https://open.larksuite.com/document)
- [Message API](https://open.larksuite.com/document/server-docs/im-v1/message)

### Helpful Links
- [Create Custom App Guide](https://open.larksuite.com/document/home/introduction-to-custom-app-development)
- [Bot Development Guide](https://open.larksuite.com/document/home/develop-a-bot)
- [Message Card Builder](https://open.larksuite.com/tool/cardbuilder)

---

## ✅ Quick Checklist

Before going live, verify:

- [ ] App created in Lark Open Platform
- [ ] All required scopes added
- [ ] App published and installed to workspace
- [ ] App ID and Secret saved to `.env`
- [ ] User Open ID obtained and saved to `.env`
- [ ] Test message sent successfully
- [ ] Messaging platform configured (`lark` or `both`)
- [ ] Personal OS running and sending updates

---

## 🎉 Success!

Once configured, you'll receive Personal OS updates in Lark:
- 📋 Daily plans every morning
- 📊 Progress checks at midday
- 🌟 Daily summaries every evening

All delivered directly to your Lark messages!

---

**Pro Tip:** Use `MESSAGING_PLATFORM=both` to receive updates in BOTH Slack and Lark for maximum visibility!
