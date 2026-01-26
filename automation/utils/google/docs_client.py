"""
Google Docs Client - Document creation and editing
"""

from typing import Optional, List, Dict, Any
from loguru import logger

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.google.base_client import google_base_client
from utils.google.drive_client import drive_client
from config import settings


class DocsClient:
    """Client for Google Docs operations"""

    def __init__(self):
        self._service = None

    @property
    def service(self):
        """Lazy initialization of Docs service"""
        if self._service is None and google_base_client.is_authenticated():
            self._service = build(
                "docs", "v1", credentials=google_base_client.credentials
            )
        return self._service

    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a document by ID.

        Args:
            document_id: The document ID

        Returns:
            Document resource dict or None
        """
        if not self.service:
            logger.warning("Docs service not initialized")
            return None

        try:
            doc = self.service.documents().get(documentId=document_id).execute()
            logger.info(f"Retrieved document: {doc.get('title')}")
            return doc
        except HttpError as e:
            logger.error(f"Failed to get document {document_id}: {e}")
            return None

    def get_document_content(self, document_id: str) -> str:
        """
        Extract plain text content from a document.

        Args:
            document_id: The document ID

        Returns:
            Plain text content of the document
        """
        doc = self.get_document(document_id)
        if not doc:
            return ""

        try:
            content = doc.get("body", {}).get("content", [])
            text_parts = []

            for element in content:
                if "paragraph" in element:
                    paragraph = element["paragraph"]
                    for elem in paragraph.get("elements", []):
                        if "textRun" in elem:
                            text_parts.append(elem["textRun"].get("content", ""))

            return "".join(text_parts)
        except Exception as e:
            logger.error(f"Failed to extract content: {e}")
            return ""

    def get_document_with_structure(self, document_id: str) -> Dict[str, Any]:
        """
        Get document content with structure (headings, paragraphs, lists, tables).

        Args:
            document_id: The document ID

        Returns:
            Structured content dict
        """
        doc = self.get_document(document_id)
        if not doc:
            return {}

        try:
            result = {
                "title": doc.get("title", ""),
                "document_id": document_id,
                "sections": [],
                "tables": [],
                "lists": [],
            }

            content = doc.get("body", {}).get("content", [])
            current_section = {"heading": None, "paragraphs": []}

            for element in content:
                if "paragraph" in element:
                    paragraph = element["paragraph"]
                    style = paragraph.get("paragraphStyle", {})
                    named_style = style.get("namedStyleType", "")

                    # Extract text
                    text = ""
                    for elem in paragraph.get("elements", []):
                        if "textRun" in elem:
                            text += elem["textRun"].get("content", "")

                    text = text.strip()
                    if not text:
                        continue

                    # Check if it's a heading
                    if named_style.startswith("HEADING"):
                        # Save previous section
                        if current_section["heading"] or current_section["paragraphs"]:
                            result["sections"].append(current_section)
                        current_section = {"heading": text, "level": named_style, "paragraphs": []}
                    else:
                        current_section["paragraphs"].append(text)

                elif "table" in element:
                    table = element["table"]
                    table_data = self._extract_table(table)
                    result["tables"].append(table_data)

            # Add last section
            if current_section["heading"] or current_section["paragraphs"]:
                result["sections"].append(current_section)

            return result

        except Exception as e:
            logger.error(f"Failed to parse document structure: {e}")
            return {}

    def _extract_table(self, table: Dict) -> List[List[str]]:
        """Extract table data as 2D list"""
        rows = []
        for row in table.get("tableRows", []):
            cells = []
            for cell in row.get("tableCells", []):
                cell_text = ""
                for content in cell.get("content", []):
                    if "paragraph" in content:
                        for elem in content["paragraph"].get("elements", []):
                            if "textRun" in elem:
                                cell_text += elem["textRun"].get("content", "")
                cells.append(cell_text.strip())
            rows.append(cells)
        return rows

    def create_document(
        self,
        title: str,
        content: Optional[str] = None,
        folder_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a new document.

        Args:
            title: Document title
            content: Initial content (plain text)
            folder_id: Folder to create in

        Returns:
            Document ID or None
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would create document: {title}")
            return "dry_run_doc_id"

        if not self.service:
            return None

        try:
            # Create empty document
            doc = self.service.documents().create(body={"title": title}).execute()
            doc_id = doc.get("documentId")
            logger.info(f"Created document '{title}' with ID: {doc_id}")

            # Add content if provided
            if content:
                self.append_text(doc_id, content)

            # Move to folder if specified
            if folder_id and drive_client.service:
                drive_client.service.files().update(
                    fileId=doc_id,
                    addParents=folder_id,
                    fields="id, parents",
                ).execute()

            return doc_id

        except HttpError as e:
            logger.error(f"Failed to create document: {e}")
            return None

    def append_text(
        self,
        document_id: str,
        text: str,
        index: Optional[int] = None,
    ) -> bool:
        """
        Append text to a document.

        Args:
            document_id: The document ID
            text: Text to append
            index: Position to insert (None for end)

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would append text to {document_id}")
            return True

        if not self.service:
            return False

        try:
            # Get document to find end index if not specified
            if index is None:
                doc = self.get_document(document_id)
                if doc:
                    content = doc.get("body", {}).get("content", [])
                    if content:
                        index = content[-1].get("endIndex", 1) - 1
                    else:
                        index = 1

            requests = [
                {
                    "insertText": {
                        "location": {"index": index},
                        "text": text,
                    }
                }
            ]

            self.service.documents().batchUpdate(
                documentId=document_id,
                body={"requests": requests},
            ).execute()

            logger.info(f"Appended text to document {document_id}")
            return True

        except HttpError as e:
            logger.error(f"Failed to append text: {e}")
            return False

    def replace_text(
        self,
        document_id: str,
        find_text: str,
        replace_text: str,
        match_case: bool = False,
    ) -> bool:
        """
        Find and replace text in a document.

        Args:
            document_id: The document ID
            find_text: Text to find
            replace_text: Replacement text
            match_case: Case-sensitive matching

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would replace '{find_text}' in {document_id}")
            return True

        if not self.service:
            return False

        try:
            requests = [
                {
                    "replaceAllText": {
                        "containsText": {
                            "text": find_text,
                            "matchCase": match_case,
                        },
                        "replaceText": replace_text,
                    }
                }
            ]

            self.service.documents().batchUpdate(
                documentId=document_id,
                body={"requests": requests},
            ).execute()

            logger.info(f"Replaced text in document {document_id}")
            return True

        except HttpError as e:
            logger.error(f"Failed to replace text: {e}")
            return False

    def add_heading(
        self,
        document_id: str,
        text: str,
        level: int = 1,
    ) -> bool:
        """
        Add a heading to the document.

        Args:
            document_id: The document ID
            text: Heading text
            level: Heading level (1-6)

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would add heading to {document_id}")
            return True

        if not self.service:
            return False

        try:
            # Get end index
            doc = self.get_document(document_id)
            if not doc:
                return False

            content = doc.get("body", {}).get("content", [])
            end_index = content[-1].get("endIndex", 1) - 1 if content else 1

            # Insert text then format as heading
            heading_style = f"HEADING_{min(level, 6)}"
            requests = [
                {
                    "insertText": {
                        "location": {"index": end_index},
                        "text": f"{text}\n",
                    }
                },
                {
                    "updateParagraphStyle": {
                        "range": {
                            "startIndex": end_index,
                            "endIndex": end_index + len(text) + 1,
                        },
                        "paragraphStyle": {"namedStyleType": heading_style},
                        "fields": "namedStyleType",
                    }
                },
            ]

            self.service.documents().batchUpdate(
                documentId=document_id,
                body={"requests": requests},
            ).execute()

            return True

        except HttpError as e:
            logger.error(f"Failed to add heading: {e}")
            return False


# Global Docs client instance
docs_client = DocsClient()


if __name__ == "__main__":
    print("Testing Google Docs Client...")
    print("=" * 50)

    if docs_client.service:
        print("Docs service initialized successfully")

        # Test creating a document (dry run)
        if settings.dry_run:
            doc_id = docs_client.create_document("Test Document", "Hello, World!")
            print(f"Created document: {doc_id}")
    else:
        print("Docs service not initialized - check credentials")

    print("\n" + "=" * 50)
