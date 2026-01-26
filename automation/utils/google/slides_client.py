"""
Google Slides Client - Presentation management
"""

from typing import Optional, List, Dict, Any
from loguru import logger

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.google.base_client import google_base_client
from utils.google.drive_client import drive_client
from config import settings


class SlidesClient:
    """Client for Google Slides operations"""

    def __init__(self):
        self._service = None

    @property
    def service(self):
        """Lazy initialization of Slides service"""
        if self._service is None and google_base_client.is_authenticated():
            self._service = build(
                "slides", "v1", credentials=google_base_client.credentials
            )
        return self._service

    def get_presentation(self, presentation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a presentation by ID.

        Args:
            presentation_id: The presentation ID

        Returns:
            Presentation resource dict or None
        """
        if not self.service:
            logger.warning("Slides service not initialized")
            return None

        try:
            presentation = self.service.presentations().get(
                presentationId=presentation_id
            ).execute()
            logger.info(f"Retrieved presentation: {presentation.get('title')}")
            return presentation
        except HttpError as e:
            logger.error(f"Failed to get presentation {presentation_id}: {e}")
            return None

    def get_slide_content(self, presentation_id: str) -> List[Dict[str, Any]]:
        """
        Extract content from all slides.

        Args:
            presentation_id: The presentation ID

        Returns:
            List of slide content dicts
        """
        presentation = self.get_presentation(presentation_id)
        if not presentation:
            return []

        slides_content = []
        slides = presentation.get("slides", [])

        for i, slide in enumerate(slides):
            slide_data = {
                "slide_number": i + 1,
                "slide_id": slide.get("objectId"),
                "texts": [],
                "notes": "",
            }

            # Extract text from page elements
            for element in slide.get("pageElements", []):
                if "shape" in element:
                    shape = element["shape"]
                    if "text" in shape:
                        text = self._extract_text_from_text_elements(
                            shape["text"].get("textElements", [])
                        )
                        if text.strip():
                            slide_data["texts"].append(text.strip())

                elif "table" in element:
                    # Extract table content
                    table = element["table"]
                    table_text = self._extract_table_content(table)
                    if table_text:
                        slide_data["texts"].append(table_text)

            # Extract speaker notes
            if "slideProperties" in slide:
                notes_page = slide["slideProperties"].get("notesPage", {})
                for element in notes_page.get("pageElements", []):
                    if "shape" in element:
                        shape = element["shape"]
                        if shape.get("shapeType") == "TEXT_BOX" and "text" in shape:
                            notes = self._extract_text_from_text_elements(
                                shape["text"].get("textElements", [])
                            )
                            slide_data["notes"] = notes.strip()

            slides_content.append(slide_data)

        return slides_content

    def _extract_text_from_text_elements(self, text_elements: List[Dict]) -> str:
        """Extract plain text from text elements"""
        text_parts = []
        for element in text_elements:
            if "textRun" in element:
                text_parts.append(element["textRun"].get("content", ""))
        return "".join(text_parts)

    def _extract_table_content(self, table: Dict) -> str:
        """Extract text content from a table"""
        rows = []
        for row in table.get("tableRows", []):
            cells = []
            for cell in row.get("tableCells", []):
                cell_text = ""
                if "text" in cell:
                    cell_text = self._extract_text_from_text_elements(
                        cell["text"].get("textElements", [])
                    )
                cells.append(cell_text.strip())
            rows.append(" | ".join(cells))
        return "\n".join(rows)

    def get_presentation_text(self, presentation_id: str) -> str:
        """
        Get all text from a presentation as a single string.

        Args:
            presentation_id: The presentation ID

        Returns:
            Combined text content
        """
        slides = self.get_slide_content(presentation_id)
        text_parts = []

        for slide in slides:
            text_parts.append(f"--- Slide {slide['slide_number']} ---")
            text_parts.extend(slide["texts"])
            if slide["notes"]:
                text_parts.append(f"[Notes: {slide['notes']}]")
            text_parts.append("")

        return "\n".join(text_parts)

    def create_presentation(
        self,
        title: str,
        folder_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a new presentation.

        Args:
            title: Presentation title
            folder_id: Folder to create in

        Returns:
            Presentation ID or None
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would create presentation: {title}")
            return "dry_run_presentation_id"

        if not self.service:
            return None

        try:
            presentation = self.service.presentations().create(
                body={"title": title}
            ).execute()

            presentation_id = presentation.get("presentationId")
            logger.info(f"Created presentation '{title}' with ID: {presentation_id}")

            # Move to folder if specified
            if folder_id and drive_client.service:
                drive_client.service.files().update(
                    fileId=presentation_id,
                    addParents=folder_id,
                    fields="id, parents",
                ).execute()

            return presentation_id

        except HttpError as e:
            logger.error(f"Failed to create presentation: {e}")
            return None

    def add_slide(
        self,
        presentation_id: str,
        layout: str = "BLANK",
        insertion_index: Optional[int] = None,
    ) -> Optional[str]:
        """
        Add a new slide to a presentation.

        Args:
            presentation_id: The presentation ID
            layout: Slide layout type
            insertion_index: Position to insert (None for end)

        Returns:
            New slide ID or None
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would add slide to {presentation_id}")
            return "dry_run_slide_id"

        if not self.service:
            return None

        try:
            requests = [{
                "createSlide": {
                    "slideLayoutReference": {
                        "predefinedLayout": layout
                    }
                }
            }]

            if insertion_index is not None:
                requests[0]["createSlide"]["insertionIndex"] = insertion_index

            response = self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={"requests": requests},
            ).execute()

            slide_id = response.get("replies", [{}])[0].get("createSlide", {}).get("objectId")
            logger.info(f"Added slide with ID: {slide_id}")
            return slide_id

        except HttpError as e:
            logger.error(f"Failed to add slide: {e}")
            return None

    def add_text_box(
        self,
        presentation_id: str,
        slide_id: str,
        text: str,
        x: float = 100,
        y: float = 100,
        width: float = 400,
        height: float = 100,
    ) -> bool:
        """
        Add a text box to a slide.

        Args:
            presentation_id: The presentation ID
            slide_id: The slide ID
            text: Text content
            x, y: Position in points
            width, height: Size in points

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would add text box to slide {slide_id}")
            return True

        if not self.service:
            return False

        try:
            element_id = f"textbox_{slide_id}_{x}_{y}"

            requests = [
                {
                    "createShape": {
                        "objectId": element_id,
                        "shapeType": "TEXT_BOX",
                        "elementProperties": {
                            "pageObjectId": slide_id,
                            "size": {
                                "width": {"magnitude": width, "unit": "PT"},
                                "height": {"magnitude": height, "unit": "PT"},
                            },
                            "transform": {
                                "scaleX": 1,
                                "scaleY": 1,
                                "translateX": x,
                                "translateY": y,
                                "unit": "PT",
                            },
                        },
                    }
                },
                {
                    "insertText": {
                        "objectId": element_id,
                        "text": text,
                    }
                },
            ]

            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={"requests": requests},
            ).execute()

            logger.info(f"Added text box to slide {slide_id}")
            return True

        except HttpError as e:
            logger.error(f"Failed to add text box: {e}")
            return False

    def replace_text(
        self,
        presentation_id: str,
        find_text: str,
        replace_text: str,
        match_case: bool = False,
    ) -> bool:
        """
        Find and replace text in a presentation.

        Args:
            presentation_id: The presentation ID
            find_text: Text to find
            replace_text: Replacement text
            match_case: Case-sensitive matching

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would replace '{find_text}' in {presentation_id}")
            return True

        if not self.service:
            return False

        try:
            requests = [{
                "replaceAllText": {
                    "containsText": {
                        "text": find_text,
                        "matchCase": match_case,
                    },
                    "replaceText": replace_text,
                }
            }]

            self.service.presentations().batchUpdate(
                presentationId=presentation_id,
                body={"requests": requests},
            ).execute()

            logger.info(f"Replaced text in presentation {presentation_id}")
            return True

        except HttpError as e:
            logger.error(f"Failed to replace text: {e}")
            return False


# Global Slides client instance
slides_client = SlidesClient()


if __name__ == "__main__":
    print("Testing Google Slides Client...")
    print("=" * 50)

    if slides_client.service:
        print("Slides service initialized successfully")
    else:
        print("Slides service not initialized - check credentials")

    print("\n" + "=" * 50)
