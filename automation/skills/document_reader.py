"""
Document Reader Skill - Extract content from Google Workspace documents
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from loguru import logger

from utils.google.docs_client import docs_client
from utils.google.sheets_client import sheets_client
from utils.google.slides_client import slides_client
from utils.google.drive_client import drive_client
from models.document import DocumentContent, TableData
from models.enums import DocType


class DocumentReader:
    """
    Skill for reading and extracting content from Google Workspace documents.

    Supports:
    - Google Docs
    - Google Sheets
    - Google Slides
    """

    def __init__(self):
        self.docs = docs_client
        self.sheets = sheets_client
        self.slides = slides_client
        self.drive = drive_client

    def read(self, document_id: str, doc_type: Optional[str] = None) -> Optional[DocumentContent]:
        """
        Read a document and extract its content.

        Args:
            document_id: The document ID
            doc_type: Document type ("docs", "sheets", "slides")
                     If not provided, will auto-detect

        Returns:
            DocumentContent object or None
        """
        logger.info(f"Reading document {document_id}")

        # Auto-detect type if not provided
        if not doc_type:
            doc_type = self._detect_type(document_id)

        if doc_type == "docs":
            return self._read_doc(document_id)
        elif doc_type == "sheets":
            return self._read_sheet(document_id)
        elif doc_type == "slides":
            return self._read_slides(document_id)
        else:
            logger.warning(f"Unsupported document type: {doc_type}")
            return None

    def _detect_type(self, document_id: str) -> Optional[str]:
        """Detect document type from Drive API"""
        file_info = self.drive.get_file(document_id)
        if not file_info:
            return None

        mime_type = file_info.get("mimeType", "")
        type_map = {
            "application/vnd.google-apps.document": "docs",
            "application/vnd.google-apps.spreadsheet": "sheets",
            "application/vnd.google-apps.presentation": "slides",
        }
        return type_map.get(mime_type)

    def _read_doc(self, document_id: str) -> Optional[DocumentContent]:
        """Read a Google Doc"""
        # Get metadata from Drive
        file_info = self.drive.get_file(document_id)
        if not file_info:
            logger.error(f"Could not get file info for {document_id}")
            return None

        # Get content from Docs API
        content = self.docs.get_document_content(document_id)
        structure = self.docs.get_document_with_structure(document_id)

        # Extract tables
        tables = []
        for table_data in structure.get("tables", []):
            if table_data:
                headers = table_data[0] if table_data else []
                rows = table_data[1:] if len(table_data) > 1 else []
                tables.append(TableData(headers=headers, rows=rows))

        # Parse timestamps
        created_at = None
        if file_info.get("createdTime"):
            created_at = datetime.fromisoformat(
                file_info["createdTime"].replace("Z", "+00:00")
            )

        modified_at = None
        if file_info.get("modifiedTime"):
            modified_at = datetime.fromisoformat(
                file_info["modifiedTime"].replace("Z", "+00:00")
            )

        # Get owner
        owner = ""
        if file_info.get("owners"):
            owner = file_info["owners"][0].get("emailAddress", "")

        # Get folder path
        folder_path = ""
        if file_info.get("parents"):
            folder_path = self.drive.get_folder_path(file_info["parents"][0])

        return DocumentContent(
            id=document_id,
            title=file_info.get("name", ""),
            doc_type=DocType.DOCS,
            content=content,
            tables=tables,
            created_at=created_at,
            modified_at=modified_at,
            owner=owner,
            url=file_info.get("webViewLink", ""),
            folder_path=folder_path,
        )

    def _read_sheet(
        self,
        spreadsheet_id: str,
        sheet_name: Optional[str] = None,
        range_name: Optional[str] = None,
    ) -> Optional[DocumentContent]:
        """Read a Google Sheet"""
        # Get metadata from Drive
        file_info = self.drive.get_file(spreadsheet_id)
        if not file_info:
            logger.error(f"Could not get file info for {spreadsheet_id}")
            return None

        # Get spreadsheet metadata
        spreadsheet = self.sheets.get_spreadsheet(spreadsheet_id)
        if not spreadsheet:
            return None

        # Get values
        if range_name:
            values = self.sheets.get_values(spreadsheet_id, range_name)
        elif sheet_name:
            values = self.sheets.get_all_values(spreadsheet_id, sheet_name)
        else:
            # Get first sheet
            sheets_list = spreadsheet.get("sheets", [])
            if sheets_list:
                first_sheet = sheets_list[0].get("properties", {}).get("title", "Sheet1")
                values = self.sheets.get_all_values(spreadsheet_id, first_sheet)
            else:
                values = []

        # Convert to table format
        tables = []
        if values:
            headers = values[0] if values else []
            rows = values[1:] if len(values) > 1 else []
            tables.append(TableData(headers=headers, rows=rows))

        # Convert to text content
        content_lines = []
        for row in values:
            content_lines.append("\t".join(str(cell) for cell in row))
        content = "\n".join(content_lines)

        # Parse timestamps
        created_at = None
        if file_info.get("createdTime"):
            created_at = datetime.fromisoformat(
                file_info["createdTime"].replace("Z", "+00:00")
            )

        modified_at = None
        if file_info.get("modifiedTime"):
            modified_at = datetime.fromisoformat(
                file_info["modifiedTime"].replace("Z", "+00:00")
            )

        owner = ""
        if file_info.get("owners"):
            owner = file_info["owners"][0].get("emailAddress", "")

        folder_path = ""
        if file_info.get("parents"):
            folder_path = self.drive.get_folder_path(file_info["parents"][0])

        return DocumentContent(
            id=spreadsheet_id,
            title=file_info.get("name", ""),
            doc_type=DocType.SHEETS,
            content=content,
            tables=tables,
            created_at=created_at,
            modified_at=modified_at,
            owner=owner,
            url=file_info.get("webViewLink", ""),
            folder_path=folder_path,
        )

    def _read_slides(self, presentation_id: str) -> Optional[DocumentContent]:
        """Read a Google Slides presentation"""
        # Get metadata from Drive
        file_info = self.drive.get_file(presentation_id)
        if not file_info:
            logger.error(f"Could not get file info for {presentation_id}")
            return None

        # Get presentation content
        content = self.slides.get_presentation_text(presentation_id)
        slides_content = self.slides.get_slide_content(presentation_id)

        # Extract any tables from slides
        tables = []
        # (Slides tables are already included in text content)

        # Parse timestamps
        created_at = None
        if file_info.get("createdTime"):
            created_at = datetime.fromisoformat(
                file_info["createdTime"].replace("Z", "+00:00")
            )

        modified_at = None
        if file_info.get("modifiedTime"):
            modified_at = datetime.fromisoformat(
                file_info["modifiedTime"].replace("Z", "+00:00")
            )

        owner = ""
        if file_info.get("owners"):
            owner = file_info["owners"][0].get("emailAddress", "")

        folder_path = ""
        if file_info.get("parents"):
            folder_path = self.drive.get_folder_path(file_info["parents"][0])

        return DocumentContent(
            id=presentation_id,
            title=file_info.get("name", ""),
            doc_type=DocType.SLIDES,
            content=content,
            tables=tables,
            created_at=created_at,
            modified_at=modified_at,
            owner=owner,
            url=file_info.get("webViewLink", ""),
            folder_path=folder_path,
        )

    def read_multiple(
        self,
        document_ids: List[str],
        doc_types: Optional[Dict[str, str]] = None,
    ) -> List[DocumentContent]:
        """
        Read multiple documents.

        Args:
            document_ids: List of document IDs
            doc_types: Optional dict mapping doc_id to doc_type

        Returns:
            List of DocumentContent objects
        """
        logger.info(f"Reading {len(document_ids)} documents")

        results = []
        for doc_id in document_ids:
            doc_type = doc_types.get(doc_id) if doc_types else None
            doc = self.read(doc_id, doc_type)
            if doc:
                results.append(doc)

        logger.info(f"Successfully read {len(results)} documents")
        return results

    def extract_text_only(self, document_id: str) -> str:
        """
        Extract just the text content from a document.

        Args:
            document_id: The document ID

        Returns:
            Plain text content
        """
        doc = self.read(document_id)
        return doc.content if doc else ""

    def get_document_metadata(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get document metadata without reading full content.

        Args:
            document_id: The document ID

        Returns:
            Metadata dict
        """
        return self.drive.get_file(document_id)


# Global instance
document_reader = DocumentReader()
