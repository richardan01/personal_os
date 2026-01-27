"""
Google Drive Client - File storage and management
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from loguru import logger

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

from utils.google.base_client import google_base_client
from config import settings


class DriveClient:
    """Client for Google Drive operations"""

    def __init__(self):
        self._service = None

    @property
    def service(self):
        """Lazy initialization of Drive service"""
        if self._service is None and google_base_client.is_authenticated():
            self._service = build(
                "drive", "v3", credentials=google_base_client.credentials
            )
        return self._service

    def list_files(
        self,
        folder_id: Optional[str] = None,
        query: Optional[str] = None,
        mime_type: Optional[str] = None,
        max_results: int = 100,
        order_by: str = "modifiedTime desc",
    ) -> List[Dict[str, Any]]:
        """
        List files in Drive or a specific folder.

        Args:
            folder_id: ID of folder to list (None for root)
            query: Additional query string
            mime_type: Filter by MIME type
            max_results: Maximum number of results
            order_by: Sort order

        Returns:
            List of file metadata dicts
        """
        if not self.service:
            logger.warning("Drive service not initialized")
            return []

        try:
            # Build query
            q_parts = []
            if folder_id:
                q_parts.append(f"'{folder_id}' in parents")
            if mime_type:
                q_parts.append(f"mimeType='{mime_type}'")
            if query:
                q_parts.append(query)

            q = " and ".join(q_parts) if q_parts else None

            results = []
            page_token = None

            while True:
                response = self.service.files().list(
                    q=q,
                    pageSize=min(max_results - len(results), 100),
                    fields="nextPageToken, files(id, name, mimeType, modifiedTime, createdTime, owners, webViewLink, parents)",
                    orderBy=order_by,
                    pageToken=page_token,
                ).execute()

                results.extend(response.get("files", []))

                page_token = response.get("nextPageToken")
                if not page_token or len(results) >= max_results:
                    break

            logger.info(f"Listed {len(results)} files from Drive")
            return results[:max_results]

        except HttpError as e:
            logger.error(f"Drive API error: {e}")
            return []

    def search_files(
        self,
        keywords: str,
        folder_id: Optional[str] = None,
        file_types: Optional[List[str]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Search for files by keywords and filters.

        Args:
            keywords: Search keywords
            folder_id: Limit search to folder
            file_types: List of file types ("docs", "sheets", "slides", "pdf")
            date_from: Modified after this date
            date_to: Modified before this date
            max_results: Maximum results

        Returns:
            List of matching files
        """
        if not self.service:
            return []

        try:
            # Build query parts
            q_parts = [f"fullText contains '{keywords}'"]

            if folder_id:
                q_parts.append(f"'{folder_id}' in parents")

            if file_types:
                mime_types = []
                type_map = {
                    "docs": "application/vnd.google-apps.document",
                    "sheets": "application/vnd.google-apps.spreadsheet",
                    "slides": "application/vnd.google-apps.presentation",
                    "pdf": "application/pdf",
                    "folder": "application/vnd.google-apps.folder",
                }
                for ft in file_types:
                    if ft in type_map:
                        mime_types.append(f"mimeType='{type_map[ft]}'")
                if mime_types:
                    q_parts.append(f"({' or '.join(mime_types)})")

            if date_from:
                q_parts.append(f"modifiedTime >= '{date_from.isoformat()}Z'")
            if date_to:
                q_parts.append(f"modifiedTime <= '{date_to.isoformat()}Z'")

            q_parts.append("trashed = false")

            return self.list_files(
                query=" and ".join(q_parts),
                max_results=max_results,
            )

        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    def get_file(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        Get file metadata by ID.

        Args:
            file_id: The file ID

        Returns:
            File metadata dict or None
        """
        if not self.service:
            return None

        try:
            file = self.service.files().get(
                fileId=file_id,
                fields="id, name, mimeType, modifiedTime, createdTime, owners, webViewLink, parents, description",
            ).execute()
            return file
        except HttpError as e:
            logger.error(f"Failed to get file {file_id}: {e}")
            return None

    def get_folder_path(self, folder_id: str) -> str:
        """
        Get the full path of a folder.

        Args:
            folder_id: The folder ID

        Returns:
            Full path string (e.g., "My Drive/Projects/Discovery")
        """
        if not self.service:
            return ""

        try:
            path_parts = []
            current_id = folder_id

            while current_id:
                file = self.service.files().get(
                    fileId=current_id,
                    fields="id, name, parents",
                ).execute()

                path_parts.insert(0, file.get("name", ""))
                parents = file.get("parents", [])
                current_id = parents[0] if parents else None

            return "/".join(path_parts)
        except HttpError as e:
            logger.error(f"Failed to get folder path: {e}")
            return ""

    def create_folder(
        self,
        name: str,
        parent_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a new folder.

        Args:
            name: Folder name
            parent_id: Parent folder ID (None for root)

        Returns:
            New folder ID or None
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would create folder: {name}")
            return "dry_run_folder_id"

        if not self.service:
            return None

        try:
            metadata = {
                "name": name,
                "mimeType": "application/vnd.google-apps.folder",
            }
            if parent_id:
                metadata["parents"] = [parent_id]

            folder = self.service.files().create(
                body=metadata,
                fields="id",
            ).execute()

            folder_id = folder.get("id")
            logger.info(f"Created folder '{name}' with ID: {folder_id}")
            return folder_id

        except HttpError as e:
            logger.error(f"Failed to create folder: {e}")
            return None

    def list_folders(
        self,
        parent_id: Optional[str] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        List folders in a parent folder.

        Args:
            parent_id: Parent folder ID (None for root)
            max_results: Maximum results

        Returns:
            List of folder metadata
        """
        return self.list_files(
            folder_id=parent_id,
            mime_type="application/vnd.google-apps.folder",
            max_results=max_results,
        )

    def get_files_in_folder(
        self,
        folder_id: str,
        recursive: bool = False,
        file_types: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get all files in a folder, optionally recursive.

        Args:
            folder_id: Folder ID
            recursive: Include subfolders
            file_types: Filter by file types

        Returns:
            List of file metadata
        """
        files = []

        # Get direct files
        direct_files = self.list_files(folder_id=folder_id)

        for f in direct_files:
            if f.get("mimeType") == "application/vnd.google-apps.folder":
                if recursive:
                    # Recursively get files from subfolders
                    files.extend(
                        self.get_files_in_folder(
                            f["id"], recursive=True, file_types=file_types
                        )
                    )
            else:
                # Apply file type filter
                if file_types:
                    mime_type = f.get("mimeType", "")
                    type_map = {
                        "docs": "application/vnd.google-apps.document",
                        "sheets": "application/vnd.google-apps.spreadsheet",
                        "slides": "application/vnd.google-apps.presentation",
                    }
                    if not any(type_map.get(ft) == mime_type for ft in file_types):
                        continue
                files.append(f)

        return files


# Global Drive client instance
drive_client = DriveClient()


if __name__ == "__main__":
    print("Testing Google Drive Client...")
    print("=" * 50)

    if drive_client.service:
        print("Drive service initialized successfully")

        # List recent files
        files = drive_client.list_files(max_results=5)
        print(f"\nRecent files ({len(files)}):")
        for f in files:
            print(f"  - {f['name']} ({f['mimeType']})")
    else:
        print("Drive service not initialized - check credentials")

    print("\n" + "=" * 50)
