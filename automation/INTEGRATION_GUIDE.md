# Integration Guide - Google Workspace

Personal OS integrates with Google Workspace for document management, calendar, and task tracking.

---

## Supported Google Services

### Google Drive
Search and access files stored in your Google Drive.

**Use cases:**
- Find meeting notes and documents
- Search for stakeholder-related content
- Access PRDs and specifications

### Google Docs
Read and create documents.

**Use cases:**
- Extract content from meeting notes
- Generate stakeholder reports
- Create daily plan documents

### Google Sheets
Read and write spreadsheet data.

**Use cases:**
- Store stakeholder profiles
- Track metrics and KPIs
- Export data for analysis

### Google Slides
Read presentation content.

**Use cases:**
- Extract stakeholder information from presentations
- Analyze roadmap decks
- Review strategy presentations

### Google Calendar
Access your calendar events.

**Use cases:**
- Fetch today's meetings for daily planning
- Identify stakeholder meetings
- Schedule follow-up appointments

### Google Tasks
Create and manage tasks.

**Use cases:**
- Create follow-up action items
- Track stakeholder engagement tasks
- Manage to-do lists

---

## Quick Setup

### Step 1: Create Google Cloud Project

1. Go to https://console.cloud.google.com/
2. Click **"Select a project"** > **"New Project"**
3. Name your project: `Personal OS`
4. Click **"Create"**

### Step 2: Enable APIs

Enable the following APIs in your project:

1. Go to **"APIs & Services"** > **"Enable APIs and Services"**
2. Search for and enable each of these:
   - Google Drive API
   - Google Docs API
   - Google Sheets API
   - Google Slides API
   - Google Calendar API
   - Google Tasks API

### Step 3: Create Credentials

#### Option A: OAuth 2.0 (Recommended for Personal Use)

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** > **"OAuth client ID"**
3. If prompted, configure the OAuth consent screen:
   - User Type: External (or Internal if using Google Workspace)
   - App name: `Personal OS`
   - User support email: Your email
   - Developer contact: Your email
4. Application type: **"Desktop app"**
5. Name: `Personal OS Desktop`
6. Click **"Create"**
7. Download the JSON file
8. Save as `credentials/google_credentials.json`

#### Option B: Service Account (For Server Deployment)

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** > **"Service account"**
3. Name: `personal-os-service`
4. Click **"Create and Continue"**
5. Skip roles (click **"Continue"**)
6. Click **"Done"**
7. Click on the service account email
8. Go to **"Keys"** tab
9. Click **"Add Key"** > **"Create new key"**
10. Choose **"JSON"**
11. Save as `credentials/service_account.json`

**Important for Service Account:**
- Share your Google Drive folders with the service account email
- The service account email looks like: `personal-os-service@your-project.iam.gserviceaccount.com`

---

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Google Workspace Configuration
# Choose one authentication method:

# Option A: OAuth 2.0 (for desktop/personal use)
GOOGLE_CREDENTIALS_FILE=credentials/google_credentials.json

# Option B: Service Account (for server deployment)
GOOGLE_SERVICE_ACCOUNT_FILE=credentials/service_account.json

# Required Settings
GOOGLE_CALENDAR_ID=primary  # or your-email@gmail.com

# Optional Settings
GOOGLE_DRIVE_FOLDER_ID=your-folder-id  # Folder to search for documents
GOOGLE_TASKS_LIST_ID=@default  # Task list for action items
```

### Finding Your IDs

#### Google Calendar ID
- For primary calendar: Use `primary` or your email address
- For shared calendars: Go to Calendar settings > calendar > "Integrate calendar" > Calendar ID

#### Google Drive Folder ID
1. Open the folder in Google Drive
2. Look at the URL: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
3. Copy the folder ID

#### Google Tasks List ID
- Use `@default` for the default list
- Or get the list ID via the Tasks API

---

## Authentication Flow

### First-Time OAuth Setup

When you first run Personal OS with OAuth credentials:

1. A browser window will open
2. Select your Google account
3. Review permissions and click **"Allow"**
4. The token will be saved automatically
5. Future runs will use the saved token

```bash
# First run will prompt for authentication
python main.py
```

### Token Refresh

Tokens are automatically refreshed. If you encounter authentication errors:

```bash
# Delete the token file and re-authenticate
rm credentials/token.json
python main.py
```

---

## API Scopes

Personal OS requests these permissions:

| Scope | Purpose |
|-------|---------|
| `drive` | Search and read files in Drive |
| `documents` | Read and create Google Docs |
| `spreadsheets` | Read and write Google Sheets |
| `presentations` | Read Google Slides |
| `calendar` | Read calendar events |
| `tasks` | Create and manage tasks |

---

## Testing the Integration

### Test Individual Clients

```bash
# Test Google Drive
python -c "from utils.google import GoogleDriveClient; c = GoogleDriveClient(); print(c.search_files('meeting notes'))"

# Test Google Docs
python -c "from utils.google import GoogleDocsClient; c = GoogleDocsClient(); print(c.create_document('Test Doc', 'Hello World'))"

# Test Google Calendar
python -c "from utils.google import GoogleCalendarClient; c = GoogleCalendarClient(); print(c.get_todays_events())"

# Test Google Tasks
python -c "from utils.google import GoogleTasksClient; c = GoogleTasksClient(); print(c.list_tasks())"
```

### Test Full Workflow

```bash
# Run stakeholder discovery
python agents/stakeholder_discovery_agent.py
```

---

## Common Use Cases

### Stakeholder Discovery Workflow

The Stakeholder Discovery Agent uses multiple Google services:

1. **Google Drive**: Search for meeting notes, PRDs, interview transcripts
2. **Google Docs/Sheets/Slides**: Extract content from found documents
3. **Google Tasks**: Create follow-up action items
4. **Google Docs**: Generate stakeholder analysis report

### Daily Planning Workflow

The Execution Agent uses:

1. **Google Calendar**: Fetch today's meetings
2. **Google Tasks**: Get open tasks
3. **Google Docs**: Save daily plan

---

## Troubleshooting

### "Access Denied" Errors

**For OAuth:**
- Delete `credentials/token.json` and re-authenticate
- Verify you allowed all requested permissions

**For Service Account:**
- Share the Drive folder with the service account email
- Ensure the service account has the correct role

### "API Not Enabled" Errors

1. Go to Google Cloud Console
2. Navigate to APIs & Services > Enabled APIs
3. Verify all required APIs are enabled

### "Quota Exceeded" Errors

Google APIs have usage limits:
- Drive: 20,000 queries/day
- Docs: 300 requests/minute
- Calendar: 1,000,000 queries/day

If you hit limits:
- Implement caching
- Reduce polling frequency
- Request quota increase

### "Invalid Credentials" Errors

1. Verify credentials file exists at the configured path
2. Check file permissions
3. Ensure JSON file is valid
4. For OAuth: Delete token.json and re-authenticate

---

## Security Best Practices

### Credential Storage

```bash
# Keep credentials in a separate directory
mkdir -p credentials
chmod 700 credentials

# Add to .gitignore
echo "credentials/" >> .gitignore
```

### Scope Minimization

Only request scopes you need. Edit `utils/google/base_client.py` to customize:

```python
SCOPES = [
    'https://www.googleapis.com/auth/drive.readonly',  # Read-only Drive
    # Add only what you need
]
```

### Service Account Domain Delegation

For organization-wide access:

1. Go to Google Admin Console
2. Navigate to Security > API Controls > Domain-wide Delegation
3. Add the service account client ID
4. Specify allowed scopes

---

## Advanced Configuration

### Using Multiple Accounts

You can configure different credentials for different services:

```bash
# In .env
GOOGLE_DRIVE_CREDENTIALS=credentials/drive_credentials.json
GOOGLE_CALENDAR_CREDENTIALS=credentials/calendar_credentials.json
```

### Custom Token Storage

By default, tokens are stored in `credentials/token.json`. To customize:

```python
# In your code
from utils.google import GoogleBaseClient

client = GoogleBaseClient(
    credentials_file='path/to/credentials.json',
    token_file='path/to/token.json'
)
```

### Proxy Configuration

For corporate environments with proxies:

```bash
# In .env
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
```

---

## Additional Resources

- [Google Cloud Console](https://console.cloud.google.com/)
- [Google Drive API Documentation](https://developers.google.com/drive)
- [Google Docs API Documentation](https://developers.google.com/docs)
- [Google Sheets API Documentation](https://developers.google.com/sheets)
- [Google Calendar API Documentation](https://developers.google.com/calendar)
- [Google Tasks API Documentation](https://developers.google.com/tasks)

---

## Checklist

### Initial Setup
- [ ] Created Google Cloud project
- [ ] Enabled all required APIs
- [ ] Created credentials (OAuth or Service Account)
- [ ] Downloaded credentials JSON file
- [ ] Configured `.env` file
- [ ] Tested authentication

### For Service Accounts
- [ ] Shared Drive folders with service account email
- [ ] Granted appropriate permissions

### For OAuth
- [ ] Configured OAuth consent screen
- [ ] Completed first-time authentication
- [ ] Token file created successfully

---

**Pro Tip:** Start with OAuth for development and testing, then switch to a Service Account for production deployment.
