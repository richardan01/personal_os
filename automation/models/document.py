"""
Document Models - Content extracted from Google Workspace documents
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Any

from models.enums import DocType


@dataclass
class TableData:
    """Data extracted from a table in a document"""
    headers: List[str] = field(default_factory=list)
    rows: List[List[str]] = field(default_factory=list)

    def to_dict_list(self) -> List[dict]:
        """Convert table to list of dicts using headers as keys"""
        if not self.headers:
            return []
        return [
            {self.headers[i]: row[i] if i < len(row) else ""
             for i in range(len(self.headers))}
            for row in self.rows
        ]


@dataclass
class DocumentContent:
    """Raw content extracted from a Google Workspace document"""

    # Identification
    id: str                                          # Google Doc ID
    title: str                                       # Document title
    doc_type: DocType                                # DOCS, SHEETS, SLIDES

    # Content
    content: str                                     # Extracted text content
    tables: List[TableData] = field(default_factory=list)  # Tables found

    # Metadata
    created_at: Optional[datetime] = None            # When document was created
    modified_at: Optional[datetime] = None           # Last modification time
    owner: str = ""                                  # Document owner email
    url: str = ""                                    # Direct link to document

    # Context
    folder_path: str = ""                            # e.g., "Discovery/Q1/Interviews"
    tags: List[str] = field(default_factory=list)   # User-defined tags

    def __post_init__(self):
        """Ensure doc_type is DocType enum"""
        if isinstance(self.doc_type, str):
            self.doc_type = DocType(self.doc_type)

    @property
    def word_count(self) -> int:
        """Get approximate word count"""
        return len(self.content.split())

    @property
    def is_empty(self) -> bool:
        """Check if document has no content"""
        return not self.content.strip()

    def get_sections(self) -> List[dict]:
        """
        Extract sections from document content.
        Assumes sections are separated by headings (lines starting with #).
        """
        sections = []
        current_section = {"heading": None, "content": []}

        for line in self.content.split("\n"):
            line = line.strip()
            if line.startswith("#"):
                # Save previous section
                if current_section["heading"] or current_section["content"]:
                    current_section["content"] = "\n".join(current_section["content"])
                    sections.append(current_section)
                # Start new section
                heading = line.lstrip("#").strip()
                level = len(line) - len(line.lstrip("#"))
                current_section = {"heading": heading, "level": level, "content": []}
            else:
                current_section["content"].append(line)

        # Add last section
        if current_section["heading"] or current_section["content"]:
            current_section["content"] = "\n".join(current_section["content"])
            sections.append(current_section)

        return sections

    def search(self, keyword: str, case_sensitive: bool = False) -> List[str]:
        """
        Search for keyword in document and return matching lines.

        Args:
            keyword: Text to search for
            case_sensitive: Whether search is case-sensitive

        Returns:
            List of lines containing the keyword
        """
        lines = self.content.split("\n")
        if not case_sensitive:
            keyword = keyword.lower()
            return [line for line in lines if keyword in line.lower()]
        return [line for line in lines if keyword in line]

    def to_dict(self) -> dict:
        """Convert to dictionary representation"""
        return {
            "id": self.id,
            "title": self.title,
            "doc_type": self.doc_type.value,
            "content": self.content,
            "tables": [{"headers": t.headers, "rows": t.rows} for t in self.tables],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "modified_at": self.modified_at.isoformat() if self.modified_at else None,
            "owner": self.owner,
            "url": self.url,
            "folder_path": self.folder_path,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DocumentContent":
        """Create from dictionary"""
        tables = [
            TableData(headers=t.get("headers", []), rows=t.get("rows", []))
            for t in data.get("tables", [])
        ]

        created_at = None
        if data.get("created_at"):
            created_at = datetime.fromisoformat(data["created_at"])

        modified_at = None
        if data.get("modified_at"):
            modified_at = datetime.fromisoformat(data["modified_at"])

        return cls(
            id=data["id"],
            title=data["title"],
            doc_type=DocType(data["doc_type"]),
            content=data["content"],
            tables=tables,
            created_at=created_at,
            modified_at=modified_at,
            owner=data.get("owner", ""),
            url=data.get("url", ""),
            folder_path=data.get("folder_path", ""),
            tags=data.get("tags", []),
        )
