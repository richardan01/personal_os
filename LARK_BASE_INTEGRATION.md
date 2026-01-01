# Lark Base Integration - Quick Setup Guide

Your Lark Base integration is ready! This guide will help you connect your Lark Base and start reading data for the Discovery Agent.

---

## 🎯 What You Can Do Now

✅ Read data from any Lark Base table
✅ Parse interview notes, feedback, and user research
✅ Automatically format data for Discovery Agent analysis
✅ Analyze feedback with AI insights

---

## 🚀 Quick Start (3 Steps)

### Step 1: Configure Lark App Permissions

1. Go to [Lark Open Platform](https://open.larksuite.com/)
2. Open your `Personal OS Bot` app (or create one - see LARK_SETUP.md)
3. Go to **"Permissions & Scopes"**
4. Add this scope:
   - `bitable:app` - Access to Base data

5. Click **"Save"** and **"Publish"** the app

### Step 2: Grant Base Access

1. Open your Lark Base: https://pj4w2l1pwuq.sg.larksuite.com/base/Adgxb8OxhaALzSstbuMlJsI2gQd
2. Click **"Share"** button (top right)
3. Click **"Advanced Settings"**
4. Search for your bot: `Personal OS Bot`
5. Grant **Read** permission
6. Click **"Confirm"**

### Step 3: Configure Environment

1. Open `automation/.env` file (create from `.env.example` if needed)

2. Add your Lark credentials:
   ```bash
   # Lark Integration
   LARK_APP_ID=cli_your_app_id_here
   LARK_APP_SECRET=your_app_secret_here

   # AI Provider (for analysis)
   ANTHROPIC_API_KEY=sk-ant-your-key-here  # OR
   OPENAI_API_KEY=sk-your-key-here
   ```

3. Save the file

---

## ✅ Test the Integration

Run the test script to verify everything works:

```bash
cd automation
python utils/test_lark_base.py
```

**Expected output:**
```
Testing Lark Base Integration...
==================================================
✅ Successfully parsed Base URL
✅ App Token: Adgxb8OxhaALzSstbuMlJsI2gQd
✅ Table ID: tblfeqt94MooBQ8W
✅ Retrieved 15 records from base
==================================================
```

---

## 🎨 Read Your Base Data

Use the ready-made script to fetch and analyze your data:

```bash
cd automation
python read_lark_for_discovery.py
```

This will:
1. ✅ Fetch all records from your Lark Base
2. ✅ Format them for Discovery Agent
3. ✅ Save to `lark_base_data.txt`
4. ✅ (Optional) Analyze with AI and save insights

---

## 📝 Use in Your Own Code

### Example 1: Read All Records

```python
from utils.lark_client import lark_client

# Your Base URL
url = "https://pj4w2l1pwuq.sg.larksuite.com/base/Adgxb8OxhaALzSstbuMlJsI2gQd?table=tblfeqt94MooBQ8W&view=vewhzzGdMk"

# Parse the URL
parsed = lark_client.parse_base_url(url)

# Get all records
records = lark_client.get_all_base_records(
    app_token=parsed['app_token'],
    table_id=parsed['table_id']
)

# Process records
for record in records:
    fields = record['fields']
    print(f"Interviewee: {fields.get('Name')}")
    print(f"Notes: {fields.get('Notes')}")
```

### Example 2: Search for Specific Records

```python
from utils.lark_client import lark_client

# Search for high-priority feedback
records = lark_client.search_base_records(
    app_token="your_app_token",
    table_id="your_table_id",
    filter='CurrentValue.[Priority] = "High"'
)
```

### Example 3: Get First Page Only

```python
from utils.lark_client import lark_client

# Get first 100 records
result = lark_client.get_base_records(
    app_token="your_app_token",
    table_id="your_table_id",
    page_size=100
)

records = result['items']
has_more = result['has_more']
```

---

## 🔍 Your Base Details

From your URL, I extracted:

| Field | Value |
|-------|-------|
| **App Token** | `Adgxb8OxhaALzSstbuMlJsI2gQd` |
| **Table ID** | `tblfeqt94MooBQ8W` |
| **View ID** | `vewhzzGdMk` |

These are already configured in the test scripts!

---

## 🛠 API Methods Available

### `parse_base_url(url)`
Parse a Lark Base URL to extract IDs

### `list_base_tables(app_token)`
List all tables in a base

### `get_base_records(app_token, table_id, ...)`
Get one page of records (max 500)

### `get_all_base_records(app_token, table_id, ...)`
Get ALL records (handles pagination automatically)

### `search_base_records(app_token, table_id, filter, ...)`
Search records with filters and sorting

---

## 🔐 Permissions Required

Your Lark app needs these scopes:

✅ `im:message` - Send messages
✅ `bitable:app` - **Read/write Base data** (NEW!)

---

## 🚨 Troubleshooting

### Error: "Permission denied"

**Solution:**
1. Make sure you added `bitable:app` scope to your Lark app
2. Republish the app after adding the scope
3. Grant your bot access to the specific base

### Error: "Invalid app credentials"

**Solution:**
- Check `LARK_APP_ID` and `LARK_APP_SECRET` in `.env`
- Make sure there are no extra spaces
- Verify credentials in Lark Open Platform

### Error: "Failed to get records"

**Solution:**
1. Verify the base URL is correct
2. Make sure your bot has read access to the base
3. Check that the table ID exists in the base

### No records returned (but no error)

**Solution:**
- The table might be empty
- Check if you're using the correct view_id
- Try without view_id to see all records

---

## 📚 Next Steps

### 1. Test the Integration (5 minutes)
```bash
cd automation
python utils/test_lark_base.py
```

### 2. Read Your Data (2 minutes)
```bash
python read_lark_for_discovery.py
```

### 3. Analyze with Discovery Agent (5 minutes)
- Copy the output from `lark_base_data.txt`
- Paste into Claude.ai or ChatGPT
- Use the Discovery Agent prompt from `agents/discovery-agent.md`

### 4. Automate It!
Create a scheduled job to:
- Read feedback daily from Lark Base
- Analyze with Discovery Agent
- Send insights to Slack

---

## 🎉 You're All Set!

You can now:
- ✅ Read data directly from your Lark Base
- ✅ Process interview notes and feedback
- ✅ Analyze with Discovery Agent
- ✅ Integrate into automated workflows

For more details, see:
- `automation/LARK_SETUP.md` - Full Lark integration guide
- `agents/discovery-agent.md` - Discovery Agent prompts
- `automation/utils/lark_client.py` - API documentation

---

**Questions or issues?** Check the troubleshooting section or review `LARK_SETUP.md`

