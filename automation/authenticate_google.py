#!/usr/bin/env python3
"""
Google Workspace Authentication Script
Run this to complete the OAuth2 flow and save your token.
"""

import os
import sys
from pathlib import Path

# Ensure we're in the right directory
script_dir = Path(__file__).parent
os.chdir(script_dir)

# Now import and authenticate
from utils.google.base_client import GoogleBaseClient

print("Starting Google OAuth2 authentication...")
print(f"Credentials file: {script_dir / 'credentials' / 'google_credentials.json'}")
print()

client = GoogleBaseClient()

if client.credentials:
    print("\n" + "="*50)
    print("Authentication successful!")
    print("="*50)
    print(f"Token saved to: {script_dir / 'credentials' / 'google_token.json'}")
else:
    print("\n" + "="*50)
    print("Authentication failed!")
    print("="*50)
    print("Please check your credentials file and try again.")
    sys.exit(1)
