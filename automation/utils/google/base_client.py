"""
Google Base Client - Handles authentication for all Google Workspace APIs
"""

import os
from typing import Optional, List
from pathlib import Path
from loguru import logger

from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleBaseClient:
    """Base client for Google Workspace API authentication"""

    # All scopes needed for Google Workspace integration
    SCOPES = [
        # Drive
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive.readonly",
        # Docs
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/documents.readonly",
        # Sheets
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        # Slides
        "https://www.googleapis.com/auth/presentations",
        "https://www.googleapis.com/auth/presentations.readonly",
        # Calendar
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/calendar.events",
        # Tasks
        "https://www.googleapis.com/auth/tasks",
        "https://www.googleapis.com/auth/tasks.readonly",
    ]

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        token_path: Optional[str] = None,
        service_account_path: Optional[str] = None,
        scopes: Optional[List[str]] = None,
    ):
        """
        Initialize Google authentication.

        Args:
            credentials_path: Path to OAuth2 credentials JSON file
            token_path: Path to store/load token JSON file
            service_account_path: Path to service account JSON file (alternative auth)
            scopes: List of OAuth scopes (defaults to all workspace scopes)
        """
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_CREDENTIALS_PATH", "credentials/google_credentials.json"
        )
        self.token_path = token_path or os.getenv(
            "GOOGLE_TOKEN_PATH", "credentials/google_token.json"
        )
        self.service_account_path = service_account_path or os.getenv(
            "GOOGLE_SERVICE_ACCOUNT_PATH"
        )
        self.scopes = scopes or self.SCOPES
        self._credentials: Optional[Credentials] = None

    @property
    def credentials(self) -> Optional[Credentials]:
        """Get or refresh credentials"""
        if self._credentials is None:
            self._credentials = self._get_credentials()
        elif self._credentials.expired and self._credentials.refresh_token:
            self._credentials.refresh(Request())
            self._save_token()
        return self._credentials

    def _get_credentials(self) -> Optional[Credentials]:
        """
        Get credentials using service account or OAuth2 flow.

        Priority:
        1. Service account (if path provided)
        2. Existing token file
        3. OAuth2 flow (requires user interaction)
        """
        creds = None

        # Try service account first (for automated/server use)
        if self.service_account_path and Path(self.service_account_path).exists():
            try:
                creds = service_account.Credentials.from_service_account_file(
                    self.service_account_path, scopes=self.scopes
                )
                logger.info("Authenticated using service account")
                return creds
            except Exception as e:
                logger.warning(f"Service account auth failed: {e}")

        # Try existing token
        if Path(self.token_path).exists():
            try:
                creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
                if creds and creds.valid:
                    logger.info("Authenticated using existing token")
                    return creds
                elif creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    self._save_token(creds)
                    logger.info("Token refreshed successfully")
                    return creds
            except Exception as e:
                logger.warning(f"Token load failed: {e}")

        # Fall back to OAuth2 flow
        if Path(self.credentials_path).exists():
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.scopes
                )
                creds = flow.run_local_server(port=0)
                self._save_token(creds)
                logger.info("Authenticated via OAuth2 flow")
                return creds
            except Exception as e:
                logger.error(f"OAuth2 flow failed: {e}")

        logger.warning("No valid Google credentials found")
        return None

    def _save_token(self, creds: Optional[Credentials] = None) -> None:
        """Save credentials to token file"""
        creds = creds or self._credentials
        if creds:
            try:
                # Ensure directory exists
                Path(self.token_path).parent.mkdir(parents=True, exist_ok=True)
                with open(self.token_path, "w") as token_file:
                    token_file.write(creds.to_json())
                logger.debug(f"Token saved to {self.token_path}")
            except Exception as e:
                logger.error(f"Failed to save token: {e}")

    def is_authenticated(self) -> bool:
        """Check if we have valid credentials"""
        return self.credentials is not None and self.credentials.valid


# Global base client instance
google_base_client = GoogleBaseClient()
