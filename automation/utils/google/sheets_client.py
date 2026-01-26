"""
Google Sheets Client - Spreadsheet operations
"""

from typing import Optional, List, Dict, Any, Union
from loguru import logger

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils.google.base_client import google_base_client
from utils.google.drive_client import drive_client
from config import settings


class SheetsClient:
    """Client for Google Sheets operations"""

    def __init__(self):
        self._service = None

    @property
    def service(self):
        """Lazy initialization of Sheets service"""
        if self._service is None and google_base_client.is_authenticated():
            self._service = build(
                "sheets", "v4", credentials=google_base_client.credentials
            )
        return self._service

    def get_spreadsheet(self, spreadsheet_id: str) -> Optional[Dict[str, Any]]:
        """
        Get spreadsheet metadata.

        Args:
            spreadsheet_id: The spreadsheet ID

        Returns:
            Spreadsheet resource dict or None
        """
        if not self.service:
            logger.warning("Sheets service not initialized")
            return None

        try:
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()
            logger.info(f"Retrieved spreadsheet: {spreadsheet.get('properties', {}).get('title')}")
            return spreadsheet
        except HttpError as e:
            logger.error(f"Failed to get spreadsheet {spreadsheet_id}: {e}")
            return None

    def get_values(
        self,
        spreadsheet_id: str,
        range_name: str,
        value_render_option: str = "FORMATTED_VALUE",
    ) -> List[List[Any]]:
        """
        Get values from a range.

        Args:
            spreadsheet_id: The spreadsheet ID
            range_name: A1 notation range (e.g., "Sheet1!A1:D10")
            value_render_option: How values should be rendered

        Returns:
            2D list of values
        """
        if not self.service:
            return []

        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueRenderOption=value_render_option,
            ).execute()

            values = result.get("values", [])
            logger.info(f"Retrieved {len(values)} rows from {range_name}")
            return values

        except HttpError as e:
            logger.error(f"Failed to get values: {e}")
            return []

    def get_all_values(self, spreadsheet_id: str, sheet_name: str = "Sheet1") -> List[List[Any]]:
        """
        Get all values from a sheet.

        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_name: Name of the sheet

        Returns:
            2D list of all values
        """
        return self.get_values(spreadsheet_id, sheet_name)

    def get_as_dict(
        self,
        spreadsheet_id: str,
        range_name: str,
        header_row: int = 0,
    ) -> List[Dict[str, Any]]:
        """
        Get values as list of dicts using first row as headers.

        Args:
            spreadsheet_id: The spreadsheet ID
            range_name: A1 notation range
            header_row: Row index for headers (0-based)

        Returns:
            List of dicts
        """
        values = self.get_values(spreadsheet_id, range_name)
        if not values or len(values) <= header_row:
            return []

        headers = values[header_row]
        result = []

        for row in values[header_row + 1:]:
            row_dict = {}
            for i, header in enumerate(headers):
                row_dict[header] = row[i] if i < len(row) else ""
            result.append(row_dict)

        return result

    def update_values(
        self,
        spreadsheet_id: str,
        range_name: str,
        values: List[List[Any]],
        value_input_option: str = "USER_ENTERED",
    ) -> bool:
        """
        Update values in a range.

        Args:
            spreadsheet_id: The spreadsheet ID
            range_name: A1 notation range
            values: 2D list of values to write
            value_input_option: How input data should be interpreted

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would update {range_name} in {spreadsheet_id}")
            return True

        if not self.service:
            return False

        try:
            body = {"values": values}
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                body=body,
            ).execute()

            logger.info(f"Updated {len(values)} rows in {range_name}")
            return True

        except HttpError as e:
            logger.error(f"Failed to update values: {e}")
            return False

    def append_values(
        self,
        spreadsheet_id: str,
        range_name: str,
        values: List[List[Any]],
        value_input_option: str = "USER_ENTERED",
    ) -> bool:
        """
        Append values to a sheet.

        Args:
            spreadsheet_id: The spreadsheet ID
            range_name: A1 notation range (usually just sheet name)
            values: 2D list of values to append
            value_input_option: How input data should be interpreted

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would append {len(values)} rows to {spreadsheet_id}")
            return True

        if not self.service:
            return False

        try:
            body = {"values": values}
            self.service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption=value_input_option,
                insertDataOption="INSERT_ROWS",
                body=body,
            ).execute()

            logger.info(f"Appended {len(values)} rows to {range_name}")
            return True

        except HttpError as e:
            logger.error(f"Failed to append values: {e}")
            return False

    def create_spreadsheet(
        self,
        title: str,
        sheet_names: Optional[List[str]] = None,
        folder_id: Optional[str] = None,
    ) -> Optional[str]:
        """
        Create a new spreadsheet.

        Args:
            title: Spreadsheet title
            sheet_names: Names of sheets to create
            folder_id: Folder to create in

        Returns:
            Spreadsheet ID or None
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would create spreadsheet: {title}")
            return "dry_run_sheet_id"

        if not self.service:
            return None

        try:
            # Build sheet properties
            sheets = []
            if sheet_names:
                for i, name in enumerate(sheet_names):
                    sheets.append({
                        "properties": {
                            "sheetId": i,
                            "title": name,
                        }
                    })

            body = {
                "properties": {"title": title},
            }
            if sheets:
                body["sheets"] = sheets

            spreadsheet = self.service.spreadsheets().create(body=body).execute()
            spreadsheet_id = spreadsheet.get("spreadsheetId")
            logger.info(f"Created spreadsheet '{title}' with ID: {spreadsheet_id}")

            # Move to folder if specified
            if folder_id and drive_client.service:
                drive_client.service.files().update(
                    fileId=spreadsheet_id,
                    addParents=folder_id,
                    fields="id, parents",
                ).execute()

            return spreadsheet_id

        except HttpError as e:
            logger.error(f"Failed to create spreadsheet: {e}")
            return None

    def add_sheet(
        self,
        spreadsheet_id: str,
        sheet_name: str,
    ) -> bool:
        """
        Add a new sheet to an existing spreadsheet.

        Args:
            spreadsheet_id: The spreadsheet ID
            sheet_name: Name of the new sheet

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would add sheet '{sheet_name}' to {spreadsheet_id}")
            return True

        if not self.service:
            return False

        try:
            requests = [{
                "addSheet": {
                    "properties": {"title": sheet_name}
                }
            }]

            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"requests": requests},
            ).execute()

            logger.info(f"Added sheet '{sheet_name}' to spreadsheet")
            return True

        except HttpError as e:
            logger.error(f"Failed to add sheet: {e}")
            return False

    def clear_range(
        self,
        spreadsheet_id: str,
        range_name: str,
    ) -> bool:
        """
        Clear values in a range.

        Args:
            spreadsheet_id: The spreadsheet ID
            range_name: A1 notation range

        Returns:
            True if successful
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would clear {range_name} in {spreadsheet_id}")
            return True

        if not self.service:
            return False

        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=spreadsheet_id,
                range=range_name,
            ).execute()

            logger.info(f"Cleared {range_name}")
            return True

        except HttpError as e:
            logger.error(f"Failed to clear range: {e}")
            return False


# Global Sheets client instance
sheets_client = SheetsClient()


if __name__ == "__main__":
    print("Testing Google Sheets Client...")
    print("=" * 50)

    if sheets_client.service:
        print("Sheets service initialized successfully")
    else:
        print("Sheets service not initialized - check credentials")

    print("\n" + "=" * 50)
