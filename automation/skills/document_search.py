"""
Document Search Skill - Find documents in Google Drive
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from loguru import logger

from utils.google.drive_client import drive_client
from models.document import DocumentContent
from models.enums import DocType


class DocumentSearch:
    """
    Skill for searching and finding documents in Google Drive.

    This skill provides methods to:
    - Search by keywords
    - Filter by folder, file type, date range
    - Find meeting notes and interview transcripts
    - Get recent documents
    """

    def __init__(self):
        self.drive = drive_client

    def search(
        self,
        keywords: str,
        folder_id: Optional[str] = None,
        file_types: Optional[List[str]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Search for documents by keywords and filters.

        Args:
            keywords: Search keywords
            folder_id: Limit search to folder
            file_types: List of file types ("docs", "sheets", "slides", "pdf")
            date_from: Modified after this date
            date_to: Modified before this date
            max_results: Maximum results

        Returns:
            List of document metadata dicts
        """
        logger.info(f"Searching for documents with keywords: '{keywords}'")

        results = self.drive.search_files(
            keywords=keywords,
            folder_id=folder_id,
            file_types=file_types,
            date_from=date_from,
            date_to=date_to,
            max_results=max_results,
        )

        logger.info(f"Found {len(results)} documents")
        return results

    def search_by_stakeholder(
        self,
        stakeholder_name: str,
        folder_id: Optional[str] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Search for documents mentioning a specific stakeholder.

        Args:
            stakeholder_name: Name to search for
            folder_id: Limit search to folder
            max_results: Maximum results

        Returns:
            List of document metadata dicts
        """
        logger.info(f"Searching for documents about stakeholder: {stakeholder_name}")

        return self.search(
            keywords=stakeholder_name,
            folder_id=folder_id,
            file_types=["docs"],
            max_results=max_results,
        )

    def find_meeting_notes(
        self,
        folder_id: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        max_results: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Find meeting notes and interview transcripts.

        Args:
            folder_id: Folder to search in
            date_from: Start date
            date_to: End date
            max_results: Maximum results

        Returns:
            List of document metadata dicts
        """
        logger.info("Searching for meeting notes and interviews")

        # Search for common meeting note patterns
        keywords_list = [
            "meeting notes",
            "interview",
            "1:1",
            "discovery",
            "stakeholder",
        ]

        all_results = []
        seen_ids = set()

        for keyword in keywords_list:
            results = self.search(
                keywords=keyword,
                folder_id=folder_id,
                file_types=["docs"],
                date_from=date_from,
                date_to=date_to,
                max_results=max_results // len(keywords_list),
            )

            for doc in results:
                if doc["id"] not in seen_ids:
                    all_results.append(doc)
                    seen_ids.add(doc["id"])

        logger.info(f"Found {len(all_results)} meeting notes/interviews")
        return all_results[:max_results]

    def get_recent_documents(
        self,
        days: int = 7,
        folder_id: Optional[str] = None,
        file_types: Optional[List[str]] = None,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Get recently modified documents.

        Args:
            days: Number of days to look back
            folder_id: Limit to folder
            file_types: Filter by file types
            max_results: Maximum results

        Returns:
            List of document metadata dicts
        """
        logger.info(f"Getting documents modified in the last {days} days")

        date_from = datetime.utcnow() - timedelta(days=days)

        if folder_id:
            results = self.drive.get_files_in_folder(
                folder_id=folder_id,
                recursive=True,
                file_types=file_types,
            )
            # Filter by date
            results = [
                r for r in results
                if r.get("modifiedTime") and
                datetime.fromisoformat(r["modifiedTime"].replace("Z", "+00:00")) >= date_from
            ]
        else:
            results = self.drive.search_files(
                keywords="",
                file_types=file_types,
                date_from=date_from,
                max_results=max_results,
            )

        logger.info(f"Found {len(results)} recent documents")
        return results[:max_results]

    def get_folder_contents(
        self,
        folder_id: str,
        recursive: bool = False,
        file_types: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get all documents in a folder.

        Args:
            folder_id: Folder ID
            recursive: Include subfolders
            file_types: Filter by file types

        Returns:
            List of document metadata dicts
        """
        logger.info(f"Getting contents of folder {folder_id}")

        results = self.drive.get_files_in_folder(
            folder_id=folder_id,
            recursive=recursive,
            file_types=file_types,
        )

        logger.info(f"Found {len(results)} documents in folder")
        return results

    def find_by_title(
        self,
        title_pattern: str,
        folder_id: Optional[str] = None,
        max_results: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Find documents by title pattern.

        Args:
            title_pattern: Pattern to match in title
            folder_id: Limit to folder
            max_results: Maximum results

        Returns:
            List of matching documents
        """
        logger.info(f"Searching for documents with title pattern: '{title_pattern}'")

        # Build query for title search
        query = f"name contains '{title_pattern}'"

        results = self.drive.list_files(
            folder_id=folder_id,
            query=query,
            max_results=max_results,
        )

        logger.info(f"Found {len(results)} documents matching title pattern")
        return results

    def get_discovery_folder_structure(
        self,
        root_folder_id: str,
    ) -> Dict[str, Any]:
        """
        Get the structure of a discovery folder (folders and files).

        Args:
            root_folder_id: Root folder ID

        Returns:
            Nested dict of folder structure
        """
        logger.info(f"Getting folder structure for {root_folder_id}")

        def build_structure(folder_id: str, depth: int = 0) -> Dict[str, Any]:
            if depth > 5:  # Prevent infinite recursion
                return {}

            items = self.drive.list_files(folder_id=folder_id)

            structure = {
                "folders": [],
                "files": [],
            }

            for item in items:
                if item.get("mimeType") == "application/vnd.google-apps.folder":
                    folder_structure = build_structure(item["id"], depth + 1)
                    folder_structure["name"] = item["name"]
                    folder_structure["id"] = item["id"]
                    structure["folders"].append(folder_structure)
                else:
                    structure["files"].append({
                        "name": item["name"],
                        "id": item["id"],
                        "mimeType": item.get("mimeType"),
                        "modifiedTime": item.get("modifiedTime"),
                    })

            return structure

        return build_structure(root_folder_id)


# Global instance
document_search = DocumentSearch()
