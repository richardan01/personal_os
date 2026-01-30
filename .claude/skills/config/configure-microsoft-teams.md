# /configure-microsoft-teams

> Interactive setup wizard for Microsoft 365 integration - configure Teams, OneDrive, Outlook, SharePoint, and Office documents access.

## Overview

This command guides you through setting up Microsoft 365 integration step-by-step. You'll:
1. Create an Azure AD App Registration
2. Configure API permissions for Microsoft Graph
3. Generate client secret
4. Save credentials securely
5. Update environment variables
6. Test the connection

**Time required:** ~15-20 minutes

---

## When to Use

- First-time setup of Microsoft 365 integration
- Resetting Microsoft credentials
- Troubleshooting Microsoft Graph API access issues
- Adding additional Microsoft services

---

## Workflow

### Step 1: Welcome & Status Check

First, check the current Microsoft 365 configuration status.

```
📊 Microsoft 365 Configuration Status

Checking current setup...

App Registration: {status}
Credentials file: {status}
.env configuration: {status}

Ready to begin setup? Let's get started!
```

**Actions:**
1. Check if `credentials/microsoft_credentials.json` exists using Read tool
2. Check if `credentials/microsoft_token.json` exists using Read tool
3. Read `automation/.env` to check MICROSOFT_CLIENT_ID value
4. Display status for each item

---

### Step 2: Azure AD App Registration Guide

Provide detailed instructions for creating an Azure AD App Registration.

```
🔧 Azure AD App Registration

Follow these steps in the Azure Portal:

**Step 1: Create App Registration**
1. Go to: https://portal.azure.com/
2. Sign in with your Microsoft 365 account
3. Search for "App registrations" in the top search bar
4. Click "App registrations" service
5. Click "+ New registration"
6. Fill in:
   - Name: "Personal OS"
   - Supported account types: "Accounts in this organizational directory only"
   - Redirect URI: Leave blank (we'll use desktop app flow)
7. Click "Register"

**Step 2: Note Your Application IDs**
After registration, you'll see the overview page. **Copy these values:**

Application (client) ID: ___________________________
Directory (tenant) ID: ____________________________

**Keep these handy - you'll need them in Step 3!**

**Step 3: Create Client Secret**
1. In the left menu, click "Certificates & secrets"
2. Click "+ New client secret"
3. Description: "Personal OS Desktop"
4. Expires: "24 months" (recommended)
5. Click "Add"
6. **IMPORTANT**: Copy the secret VALUE immediately (it won't be shown again!)

Client Secret: _____________________________________

⚠️  **Save this secret securely - you cannot view it again after leaving this page!**

**Step 4: Configure API Permissions**
1. In the left menu, click "API permissions"
2. Click "+ Add a permission"
3. Select "Microsoft Graph"
4. Select "Delegated permissions"
5. Add these permissions:

**OneDrive & File Access:**
□ Files.Read.All
□ Files.ReadWrite.All

**Calendar & Email:**
□ Calendars.Read
□ Calendars.ReadWrite
□ Mail.Read
□ Mail.Send

**Teams:**
□ Team.ReadBasic.All
□ ChannelMessage.Read.All
□ Chat.Read

**SharePoint:**
□ Sites.Read.All
□ Sites.ReadWrite.All

**Core:**
□ User.Read
□ offline_access

6. Click "Add permissions"
7. Click "Grant admin consent for [Your Organization]"
8. Click "Yes" to confirm

✅ Once all permissions show "Granted", you're done!

**Step 5: Enable Public Client Flow**
1. In the left menu, click "Authentication"
2. Scroll to "Advanced settings"
3. Find "Allow public client flows"
4. Set to "Yes"
5. Click "Save"

✅ Once you've completed these steps, come back here!
```

**Actions:**
- Use AskUserQuestion to confirm user has completed the steps
- Options: "I've completed the setup" or "I need help with a specific step"

---

### Step 3: Collect Credentials

Interactively collect the Application ID, Tenant ID, and Client Secret.

```
📋 Collect Microsoft Credentials

I need the three values you copied from Azure Portal:

1. Application (client) ID
2. Directory (tenant) ID
3. Client secret value

Let's collect them one by one.
```

**Actions:**
1. Use AskUserQuestion: "What is your Application (client) ID? (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)"
2. Validate it's a valid GUID format
3. Use AskUserQuestion: "What is your Directory (tenant) ID? (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)"
4. Validate it's a valid GUID format
5. Use AskUserQuestion: "What is your Client secret value?"
6. Validate it's not empty

**Validation:**
- Check Application ID is valid GUID format
- Check Tenant ID is valid GUID format
- Check Client Secret is provided

---

### Step 4: Save Credentials

Save the credentials to a JSON file.

```
💾 Saving Microsoft Credentials

Creating credentials file with your app registration details...

Credentials will be saved to:
automation/credentials/microsoft_credentials.json

This file contains:
- Application (client) ID
- Directory (tenant) ID
- Client secret (encrypted)
- Authority URL
```

**Actions:**
1. Create `automation/credentials/` directory if it doesn't exist (use Bash: `mkdir -p`)
2. Create JSON structure:
```json
{
  "client_id": "{user_provided_client_id}",
  "tenant_id": "{user_provided_tenant_id}",
  "client_secret": "{user_provided_secret}",
  "authority": "https://login.microsoftonline.com/{tenant_id}",
  "scopes": [
    "Files.Read.All",
    "Files.ReadWrite.All",
    "Calendars.Read",
    "Calendars.ReadWrite",
    "Mail.Read",
    "Team.ReadBasic.All",
    "Sites.Read.All",
    "User.Read",
    "offline_access"
  ]
}
```
3. Save using Write tool to `automation/credentials/microsoft_credentials.json`
4. Confirm saved successfully

---

### Step 5: Update Environment Variables

Update the .env file with Microsoft 365 configuration.

```
⚙️ Updating Environment Configuration

Configuring automation/.env with Microsoft 365 settings...

Setting MICROSOFT_CLIENT_ID=...
Setting MICROSOFT_TENANT_ID=...
Setting MICROSOFT_CLIENT_SECRET=...
Setting MICROSOFT_CREDENTIALS_PATH=credentials/microsoft_credentials.json
Setting MICROSOFT_TOKEN_PATH=credentials/microsoft_token.json
```

**Actions:**
1. Use Edit tool to update `automation/.env`:
   - Set `MICROSOFT_CLIENT_ID={user_provided_client_id}`
   - Set `MICROSOFT_TENANT_ID={user_provided_tenant_id}`
   - Set `MICROSOFT_CLIENT_SECRET={user_provided_secret}`
   - Set `MICROSOFT_CREDENTIALS_PATH=credentials/microsoft_credentials.json`
   - Set `MICROSOFT_TOKEN_PATH=credentials/microsoft_token.json`
2. Confirm updates complete

---

### Step 6: Authentication Flow

Explain the MSAL authentication process.

```
🔐 Authenticate with Microsoft

Next step: Complete the MSAL authentication flow.

**What will happen:**
1. A browser window will open
2. You'll be asked to sign in to your Microsoft account
3. Microsoft will ask you to grant permissions to Personal OS
4. After approval, authentication will be complete
5. A token cache file will be saved for future use

**Required permissions:**
- Read and write OneDrive files
- Read and write Outlook calendar and email
- Read Teams messages and channels
- Read SharePoint sites
- Access Office documents (Word, Excel, PowerPoint)

**Note:** This is a one-time setup. The token will be refreshed automatically.

To complete authentication, you'll need to run:
```bash
cd automation
python -c "from utils.microsoft.base_client import microsoft_base_client; print('Authentication successful!' if microsoft_base_client.is_authenticated() else 'Authentication failed')"
```

A browser window will open - sign in and grant permissions.

Once you see "Authentication successful!", the setup is complete!
```

**Actions:**
- Provide the command for user to run
- Explain what to expect
- No actual authentication in this step (user runs command themselves)

---

### Step 7: Verification & Testing

Provide test commands to verify each Microsoft Graph API works.

```
✅ Verify Microsoft 365 Integration

Run these commands to test each service:

**Test OneDrive API:**
```bash
cd automation
python -c "from utils.microsoft.onedrive_client import onedrive_client; files = onedrive_client.list_files(); print(f'✅ OneDrive API works! Found {len(files)} files')"
```

**Test Outlook Calendar API:**
```bash
cd automation
python -c "from utils.microsoft.outlook_client import outlook_client; events = outlook_client.get_todays_events(); print(f'✅ Outlook API works! Found {len(events)} events today')"
```

**Test Teams API:**
```bash
cd automation
python -c "from utils.microsoft.teams_client import teams_client; teams = teams_client.list_teams(); print(f'✅ Teams API works! Found {len(teams)} teams')"
```

**Test Office Documents API:**
```bash
cd automation
python -c "from utils.microsoft.office_client import office_client; docs = office_client.search_documents('meeting', file_types=['docx']); print(f'✅ Office API works! Found {len(docs)} Word documents')"
```

If all tests pass, you're ready to use Microsoft 365 features! 🎉

**Next steps:**
- Use agents that read Word documents from OneDrive
- Access Teams messages for stakeholder discovery
- Sync with Outlook calendar
```

**Actions:**
- Provide test commands
- No actual execution (user runs themselves)

---

### Step 8: Success Summary

Display final success message with capabilities enabled.

```
🎉 Microsoft 365 Setup Complete!

**Enabled capabilities:**
✅ OneDrive - Search and access files
✅ Office Documents - Read Word, Excel, PowerPoint from OneDrive
✅ Outlook Calendar - Access and manage events
✅ Outlook Email - Read and send emails
✅ Microsoft Teams - Read messages and channels
✅ SharePoint - Access document libraries

**Configuration saved to:**
- Credentials: automation/credentials/microsoft_credentials.json
- Token cache: automation/credentials/microsoft_token.json
- Environment: automation/.env

**You can now:**
- Read Word documents (.docx) from OneDrive
- Read Excel spreadsheets (.xlsx) from OneDrive
- Read PowerPoint presentations (.pptx) from OneDrive
- Access Teams messages for discovery
- Sync with Outlook calendar as alternative to Google Calendar

**Important:**
- Client secret expires in 24 months - you'll need to renew it
- Token is automatically refreshed as long as you use the app
- Keep credentials secure - they grant access to your Microsoft 365 data

Need help? Check automation/MICROSOFT_INTEGRATION_GUIDE.md for detailed documentation.
```

---

## Error Handling

### Invalid Client ID Format
```
❌ Invalid Application (client) ID

The Application ID must be in GUID format:
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Example: 12345678-1234-1234-1234-123456789012

Please check the ID you copied from Azure Portal and try again.
```

### Invalid Tenant ID Format
```
❌ Invalid Directory (tenant) ID

The Tenant ID must be in GUID format:
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Example: 87654321-4321-4321-4321-210987654321

Please check the ID you copied from Azure Portal and try again.
```

### Permission Not Granted
```
⚠️  Admin Consent Required

Error: The requested permissions require admin consent.

To fix:
1. Go to: https://portal.azure.com/
2. Navigate to your app registration
3. Click "API permissions"
4. Click "Grant admin consent for [Your Organization]"
5. Click "Yes" to confirm

If you don't have admin rights, ask your IT administrator to grant consent.
```

### Authentication Failed
```
❌ Authentication Failed

Possible causes:

1. **Wrong credentials**: Check your Application ID, Tenant ID, and Client Secret
2. **Public client flow not enabled**: Make sure you enabled it in Authentication settings
3. **Permissions not granted**: Verify all permissions are granted with admin consent
4. **Network issues**: Check your internet connection

To fix:
- Verify credentials in Azure Portal
- Check all permissions are granted
- Try deleting microsoft_token.json and re-authenticating
- Review the error message for specific details

Need help? Check MICROSOFT_INTEGRATION_GUIDE.md for troubleshooting.
```

### API Not Accessible
```
⚠️  API Access Denied

Error: Cannot access {API_NAME}.

Common causes:
1. **Permission missing**: The required permission wasn't granted
2. **License required**: Some features require Microsoft 365 license
3. **Service unavailable**: Microsoft service may be down

To fix:
- Check all permissions are granted in Azure Portal
- Verify your Microsoft 365 subscription includes the service
- Try again in a few minutes

Quick links:
- Check permissions: https://portal.azure.com/
- Service status: https://status.office365.com/
```

### Client Secret Expired
```
⚠️  Client Secret Expired

Your client secret has expired (they last 24 months).

To fix:
1. Go to: https://portal.azure.com/
2. Navigate to your app registration
3. Go to "Certificates & secrets"
4. Delete the old secret
5. Click "+ New client secret"
6. Copy the new secret VALUE
7. Update MICROSOFT_CLIENT_SECRET in automation/.env
8. Update credentials/microsoft_credentials.json
9. Delete credentials/microsoft_token.json
10. Re-run authentication

Set a reminder to renew in 23 months!
```

---

## Important Notes

- **Security**: Credentials are stored locally and never shared
- **Token expiry**: Tokens are automatically refreshed when expired
- **Client secret expiry**: Secrets expire after 24 months - set a renewal reminder
- **Multiple accounts**: Use different app registrations for different Microsoft accounts
- **Admin consent**: Some permissions require admin approval in organizations

---

## Troubleshooting

**"The authentication flow was cancelled"**
- Make sure you complete the sign-in process
- Try again and grant all requested permissions
- Check that public client flow is enabled

**"Invalid client"**
- Verify your Application (client) ID is correct
- Check your Tenant ID matches your organization
- Ensure client secret hasn't expired

**"Insufficient privileges"**
- Some actions require admin consent
- Contact your IT administrator to grant permissions
- Or use a personal Microsoft account (no admin needed)

**"The app is not found"**
- Make sure you're signing in with the correct Microsoft account
- Verify the app registration exists in your Azure AD
- Check the Tenant ID is correct

For more help, see: automation/MICROSOFT_INTEGRATION_GUIDE.md
