# /configure-google-workspace

> Interactive setup wizard for Google Workspace integration - configure Drive, Docs, Sheets, Slides, Calendar, and Tasks access.

## Overview

This command guides you through setting up Google Workspace integration step-by-step. You'll:
1. Create a Google Cloud Project
2. Enable required APIs
3. Configure OAuth credentials
4. Save credentials securely
5. Update environment variables
6. Test the connection

**Time required:** ~10-15 minutes

---

## When to Use

- First-time setup of Google Workspace
- Resetting Google Workspace credentials
- Troubleshooting Google API access issues
- Adding additional Google APIs

---

## Workflow

### Step 1: Welcome & Status Check

First, check the current Google Workspace configuration status.

```
📊 Google Workspace Configuration Status

Checking current setup...

Credentials file: {status}
Token file: {status}
.env configuration: {status}

Ready to begin setup? Let's get started!
```

**Actions:**
1. Check if `credentials/google_credentials.json` exists using Read tool
2. Check if `credentials/google_token.json` exists using Read tool
3. Read `automation/.env` to check GOOGLE_CREDENTIALS_PATH value
4. Display status for each item

---

### Step 2: Google Cloud Project Setup Guide

Provide detailed instructions for creating a Google Cloud Project and enabling APIs.

```
🔧 Google Cloud Project Setup

Follow these steps in the Google Cloud Console:

**Step 1: Create a Google Cloud Project**
1. Go to: https://console.cloud.google.com/
2. Click "Select a project" dropdown → "New Project"
3. Project name: "Personal OS" (or your preferred name)
4. Click "Create"
5. Wait for project creation to complete

**Step 2: Enable Required APIs**
You need to enable 6 Google APIs:

Go to: https://console.cloud.google.com/apis/library

Enable each of these APIs:
□ Google Drive API - https://console.cloud.google.com/apis/library/drive.googleapis.com
□ Google Docs API - https://console.cloud.google.com/apis/library/docs.googleapis.com
□ Google Sheets API - https://console.cloud.google.com/apis/library/sheets.googleapis.com
□ Google Slides API - https://console.cloud.google.com/apis/library/slides.googleapis.com
□ Google Calendar API - https://console.cloud.google.com/apis/library/calendar-json.googleapis.com
□ Google Tasks API - https://console.cloud.google.com/apis/library/tasks.googleapis.com

For each API:
- Click on the API name
- Click "Enable" button
- Wait for it to be enabled

**Step 3: Configure OAuth Consent Screen**
1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Select "External" user type → Click "Create"
3. Fill in:
   - App name: "Personal OS"
   - User support email: (your email)
   - Developer contact: (your email)
4. Click "Save and Continue"
5. Scopes: Click "Save and Continue" (we'll set scopes later)
6. Test users: Add your email address
7. Click "Save and Continue"
8. Review and click "Back to Dashboard"

**Step 4: Create OAuth2 Credentials**
1. Go to: https://console.cloud.google.com/apis/credentials
2. Click "+ Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name: "Personal OS Desktop"
5. Click "Create"
6. Click "Download JSON" button
7. Save the file (we'll use it in the next step)

✅ Once you've completed these steps, come back here!
```

**Actions:**
- Use AskUserQuestion to confirm user has completed the steps
- Options: "I've completed the setup" or "I need help with a specific step"

---

### Step 3: Save Credentials

Ask the user to provide the credentials JSON content.

```
📁 Save Google Workspace Credentials

I need the OAuth credentials you just downloaded from Google Cloud Console.

**How to get the credentials:**
1. Open the JSON file you downloaded in Step 4
2. Copy the entire contents (it should start with {"installed": or {"web":)
3. Paste it when prompted

The credentials will be saved securely to:
automation/credentials/google_credentials.json
```

**Actions:**
1. Use AskUserQuestion to ask: "Please paste your Google OAuth credentials JSON:"
2. Parse the JSON to validate it contains required fields
3. Create `automation/credentials/` directory if it doesn't exist (use Bash: `mkdir -p`)
4. Save credentials using Write tool to `automation/credentials/google_credentials.json`
5. Confirm saved successfully

**Validation:**
- Check JSON contains `client_id`, `client_secret`, `auth_uri`, `token_uri`
- If invalid, ask user to re-paste

---

### Step 4: Update Environment Variables

Update the .env file with Google Workspace configuration.

```
⚙️ Updating Environment Configuration

Configuring automation/.env with Google Workspace settings...

Setting GOOGLE_CREDENTIALS_PATH=credentials/google_credentials.json
Setting GOOGLE_TOKEN_PATH=credentials/google_token.json
```

**Actions:**
1. Use Edit tool to update `automation/.env`:
   - Set `GOOGLE_CREDENTIALS_PATH=credentials/google_credentials.json`
   - Set `GOOGLE_TOKEN_PATH=credentials/google_token.json`
2. Use AskUserQuestion: "What is your Google Calendar ID? (usually your Gmail address)"
3. Update `GOOGLE_CALENDAR_ID` with the user's response
4. Confirm updates complete

---

### Step 5: Authentication Flow

Explain the OAuth authentication process.

```
🔐 Authenticate with Google

Next step: Complete the OAuth authentication flow.

**What will happen:**
1. A browser window will open
2. You'll be asked to sign in to your Google account
3. Google will ask you to grant permissions to Personal OS
4. After approval, authentication will be complete
5. A token file will be saved for future use

**Required permissions:**
- Read and write Google Drive files
- Read and write Google Docs
- Read and write Google Sheets
- Read and write Google Slides
- Read and write Google Calendar events
- Read and write Google Tasks

**Note:** This is a one-time setup. The token will be refreshed automatically.

To complete authentication, you'll need to run:
```bash
cd automation
python -c "from utils.google.base_client import GoogleBaseClient; client = GoogleBaseClient(); print('Authentication successful!' if client.credentials else 'Authentication failed')"
```

Once you see "Authentication successful!", the setup is complete!
```

**Actions:**
- Provide the command for user to run
- Explain what to expect
- No actual authentication in this step (user runs command themselves)

---

### Step 6: Verification & Testing

Provide test commands to verify each API works.

```
✅ Verify Google Workspace Integration

Run these commands to test each API:

**Test Drive API:**
```bash
cd automation
python -c "from utils.google.drive_client import drive_client; files = drive_client.list_files(max_results=5); print(f'✅ Drive API works! Found {len(files)} files')"
```

**Test Calendar API:**
```bash
cd automation
python -c "from utils.google.calendar_client import calendar_client; events = calendar_client.get_todays_events(); print(f'✅ Calendar API works! Found {len(events)} events today')"
```

**Test Tasks API:**
```bash
cd automation
python -c "from utils.google.tasks_client import tasks_client; lists = tasks_client.list_task_lists(); print(f'✅ Tasks API works! Found {len(lists)} task lists')"
```

If all tests pass, you're ready to use Google Workspace features! 🎉

**Next steps:**
- Use `/daily-plan` to create plans using your Google Calendar
- Use `/discovery` to analyze Google Docs
- Use agents that integrate with Google Workspace
```

**Actions:**
- Provide test commands
- No actual execution (user runs themselves)

---

### Step 7: Success Summary

Display final success message with capabilities enabled.

```
🎉 Google Workspace Setup Complete!

**Enabled capabilities:**
✅ Google Drive - Search and access files
✅ Google Docs - Read and create documents
✅ Google Sheets - Read and write spreadsheets
✅ Google Slides - Read presentations
✅ Google Calendar - Access and manage events
✅ Google Tasks - Manage task lists

**Configuration saved to:**
- Credentials: automation/credentials/google_credentials.json
- Token: automation/credentials/google_token.json
- Environment: automation/.env

**You can now:**
- Run `/daily-plan` to generate plans using your calendar
- Use stakeholder discovery with Google Drive documents
- Automate Google Workspace workflows

Need help? Check automation/INTEGRATION_GUIDE.md for detailed documentation.
```

---

## Error Handling

### Missing Credentials File
```
❌ Credentials file not found

The credentials file doesn't exist at:
automation/credentials/google_credentials.json

Please make sure you:
1. Downloaded the OAuth credentials from Google Cloud Console
2. Pasted the complete JSON content when prompted
3. The file was saved successfully

Let's try again - paste your credentials JSON:
```

### API Not Enabled
```
⚠️  API Not Enabled

Error: The {API_NAME} is not enabled for this project.

To fix:
1. Go to: https://console.cloud.google.com/apis/library/{api}
2. Click "Enable" button
3. Wait for API to be enabled
4. Try again

Quick links:
- Drive API: https://console.cloud.google.com/apis/library/drive.googleapis.com
- Docs API: https://console.cloud.google.com/apis/library/docs.googleapis.com
- Sheets API: https://console.cloud.google.com/apis/library/sheets.googleapis.com
```

### Permission Denied
```
❌ Permission Denied

Google is denying access. Common causes:

1. **Wrong Google account**: Make sure you're signing in with the account that has access to the data
2. **Insufficient scopes**: The app needs all required permissions
3. **Credentials mismatch**: The credentials file doesn't match the OAuth consent screen

To fix:
- Delete automation/credentials/google_token.json
- Run authentication again
- Grant all requested permissions

Need more help? Check the troubleshooting guide in INTEGRATION_GUIDE.md
```

### Network Error
```
⚠️  Network Error

Couldn't connect to Google APIs.

Possible causes:
- No internet connection
- Firewall blocking Google APIs
- Google services temporarily down

Please check your connection and try again.
```

---

## Important Notes

- **Security**: Credentials are stored locally and never shared
- **Token expiry**: Tokens are automatically refreshed when expired
- **Multiple accounts**: Use different credentials for different Google accounts
- **Service accounts**: For automation, consider using Service Account credentials (advanced)

---

## Troubleshooting

**"The authentication flow failed"**
- Make sure you're using the correct Google account
- Try deleting the token file and re-authenticating
- Check that all APIs are enabled in Google Cloud Console

**"API quota exceeded"**
- Google has daily quota limits for API calls
- Check usage in: https://console.cloud.google.com/apis/dashboard
- Consider upgrading to a paid plan if needed

**"The app is blocked"**
- This happens if the OAuth consent screen is in testing mode
- Add your email to test users in Google Cloud Console
- Or verify the app (required for production use)

For more help, see: automation/INTEGRATION_GUIDE.md
