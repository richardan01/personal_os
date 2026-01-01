"""
Lark (Feishu) Client - Send messages and interact with Lark
"""

from typing import Optional, List, Dict, Any
from loguru import logger
import requests
from config import settings


class LarkClient:
    """Client for sending messages to Lark (Feishu)"""

    def __init__(self):
        if not settings.lark_app_id or not settings.lark_app_secret:
            logger.warning("Lark credentials not configured")
            self.client = None
            self.access_token = None
        else:
            self.app_id = settings.lark_app_id
            self.app_secret = settings.lark_app_secret
            self.access_token = self._get_access_token()
            logger.info("Initialized Lark client")

    def _get_access_token(self) -> Optional[str]:
        """Get tenant access token from Lark"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"

        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        try:
            response = requests.post(url, json=payload)
            result = response.json()

            if result.get("code") == 0:
                token = result.get("tenant_access_token")
                logger.info("Successfully obtained Lark access token")
                return token
            else:
                logger.error(f"Failed to get Lark access token: {result}")
                return None

        except Exception as e:
            logger.error(f"Error getting Lark access token: {e}")
            return None

    def _refresh_token_if_needed(self):
        """Refresh access token if needed"""
        if not self.access_token:
            self.access_token = self._get_access_token()

    def send_message(
        self,
        text: str,
        receive_id: Optional[str] = None,
        receive_id_type: str = "open_id",
        msg_type: str = "text",
        card: Optional[Dict] = None,
    ) -> Optional[Dict]:
        """
        Send a message to Lark

        Args:
            text: Message text (supports Lark markdown)
            receive_id: Recipient ID (user_id, open_id, or chat_id)
                       If None, sends to configured user
            receive_id_type: Type of receive_id (open_id, user_id, chat_id, email)
            msg_type: Message type (text, post, interactive, etc.)
            card: Optional interactive card content

        Returns:
            Response from Lark API or None if dry run
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would send to Lark {receive_id or settings.lark_user_id}: {text[:100]}...")
            return None

        if not self.access_token:
            logger.error("Lark client not initialized - check your configuration")
            return None

        self._refresh_token_if_needed()

        # Default to sending to configured user
        target = receive_id or settings.lark_user_id

        url = "https://open.feishu.cn/open-apis/im/v1/messages"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        # Build message content based on type
        if card:
            content = card
            msg_type = "interactive"
        else:
            content = {"text": text}

        params = {
            "receive_id_type": receive_id_type
        }

        payload = {
            "receive_id": target,
            "msg_type": msg_type,
            "content": requests.utils.quote(str(content))
        }

        try:
            response = requests.post(url, headers=headers, json=payload, params=params)
            result = response.json()

            if result.get("code") == 0:
                logger.info(f"Sent message to Lark {target}")
                return result
            else:
                logger.error(f"Lark API error: {result}")
                return None

        except Exception as e:
            logger.error(f"Error sending Lark message: {e}")
            return None

    def send_dm(self, text: str, user_id: Optional[str] = None, **kwargs) -> Optional[Dict]:
        """
        Send a direct message to a user

        Args:
            text: Message text
            user_id: User ID to send to (defaults to configured user)
            **kwargs: Additional arguments for send_message

        Returns:
            Response from Lark API or None
        """
        target_user = user_id or settings.lark_user_id
        return self.send_message(text, receive_id=target_user, receive_id_type="open_id", **kwargs)

    def send_rich_text(
        self,
        title: str,
        content: List[List[Dict]],
        receive_id: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        Send a rich text (post) message

        Args:
            title: Message title
            content: Rich text content (Lark post format)
            receive_id: Recipient ID

        Returns:
            Response from Lark API or None
        """
        post_content = {
            "zh_cn": {
                "title": title,
                "content": content
            }
        }

        return self.send_message(
            text="",
            receive_id=receive_id,
            msg_type="post",
            card=post_content
        )

    def send_card(
        self,
        header_title: str,
        elements: List[Dict],
        receive_id: Optional[str] = None,
        color: str = "blue",
    ) -> Optional[Dict]:
        """
        Send an interactive card message

        Args:
            header_title: Card header title
            elements: List of card elements (text, images, buttons, etc.)
            receive_id: Recipient ID
            color: Header color (blue, green, orange, red, etc.)

        Returns:
            Response from Lark API or None
        """
        card = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": header_title
                },
                "template": color
            },
            "elements": elements
        }

        return self.send_message(
            text="",
            receive_id=receive_id,
            card=card
        )

    def send_daily_plan(self, plan: str, receive_id: Optional[str] = None) -> Optional[Dict]:
        """
        Send daily plan in a nice format

        Args:
            plan: The daily plan text
            receive_id: Recipient ID (defaults to configured user)

        Returns:
            Response from Lark API or None
        """
        elements = [
            {
                "tag": "markdown",
                "content": plan
            }
        ]

        return self.send_card(
            header_title="📋 Your Daily Plan",
            elements=elements,
            receive_id=receive_id,
            color="blue"
        )

    def send_status_update(self, update: str, receive_id: Optional[str] = None) -> Optional[Dict]:
        """
        Send a status update

        Args:
            update: Status update text
            receive_id: Recipient ID

        Returns:
            Response from Lark API or None
        """
        elements = [
            {
                "tag": "markdown",
                "content": update
            }
        ]

        return self.send_card(
            header_title="📊 Status Update",
            elements=elements,
            receive_id=receive_id,
            color="green"
        )

    def send_alert(
        self, title: str, message: str, severity: str = "warning"
    ) -> Optional[Dict]:
        """
        Send an alert/notification

        Args:
            title: Alert title
            message: Alert message
            severity: Severity level (info, warning, error)

        Returns:
            Response from Lark API or None
        """
        colors = {
            "info": "blue",
            "warning": "orange",
            "error": "red"
        }

        emoji = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "🚨"
        }

        elements = [
            {
                "tag": "markdown",
                "content": message
            }
        ]

        return self.send_card(
            header_title=f"{emoji.get(severity, '📢')} {title}",
            elements=elements,
            receive_id=settings.lark_user_id,
            color=colors.get(severity, "orange")
        )

    def get_user_info(self, user_id: Optional[str] = None) -> Optional[Dict]:
        """Get information about a Lark user"""
        if not self.access_token:
            return None

        try:
            target_user = user_id or settings.lark_user_id
            url = f"https://open.feishu.cn/open-apis/contact/v3/users/{target_user}"

            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }

            params = {
                "user_id_type": "open_id"
            }

            response = requests.get(url, headers=headers, params=params)
            result = response.json()

            if result.get("code") == 0:
                return result.get("data", {}).get("user")
            else:
                logger.error(f"Error getting user info: {result}")
                return None

        except Exception as e:
            logger.error(f"Error getting Lark user info: {e}")
            return None

    # ==================== Lark Base (Bitable) API Methods ====================

    def list_base_tables(self, app_token: str) -> Optional[List[Dict]]:
        """
        List all tables in a Lark Base

        Args:
            app_token: The Base app token (from Base URL)

        Returns:
            List of table information or None if error
        """
        if not self.access_token:
            logger.error("Lark client not initialized")
            return None

        self._refresh_token_if_needed()

        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.get(url, headers=headers)
            result = response.json()

            if result.get("code") == 0:
                tables = result.get("data", {}).get("items", [])
                logger.info(f"Found {len(tables)} tables in base {app_token}")
                return tables
            else:
                logger.error(f"Error listing tables: {result}")
                return None

        except Exception as e:
            logger.error(f"Error listing base tables: {e}")
            return None

    def get_base_records(
        self,
        app_token: str,
        table_id: str,
        page_size: int = 100,
        page_token: Optional[str] = None,
        view_id: Optional[str] = None,
        filter: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        Get records from a Lark Base table

        Args:
            app_token: The Base app token (from Base URL)
            table_id: The table ID
            page_size: Number of records per page (max 500, default 100)
            page_token: Token for pagination
            view_id: Optional view ID to filter records
            filter: Optional filter formula

        Returns:
            Dict with 'items' (records) and 'has_more' (pagination) or None
        """
        if not self.access_token:
            logger.error("Lark client not initialized")
            return None

        self._refresh_token_if_needed()

        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        params = {
            "page_size": min(page_size, 500)  # Max 500 per request
        }

        if page_token:
            params["page_token"] = page_token
        if view_id:
            params["view_id"] = view_id
        if filter:
            params["filter"] = filter

        try:
            response = requests.get(url, headers=headers, params=params)
            result = response.json()

            if result.get("code") == 0:
                data = result.get("data", {})
                records = data.get("items", [])
                has_more = data.get("has_more", False)
                next_page_token = data.get("page_token")

                logger.info(f"Retrieved {len(records)} records from table {table_id}")

                return {
                    "items": records,
                    "has_more": has_more,
                    "page_token": next_page_token
                }
            else:
                logger.error(f"Error getting records: {result}")
                return None

        except Exception as e:
            logger.error(f"Error getting base records: {e}")
            return None

    def get_all_base_records(
        self,
        app_token: str,
        table_id: str,
        view_id: Optional[str] = None,
        filter: Optional[str] = None,
        max_records: Optional[int] = None,
    ) -> Optional[List[Dict]]:
        """
        Get all records from a Lark Base table (handles pagination automatically)

        Args:
            app_token: The Base app token
            table_id: The table ID
            view_id: Optional view ID
            filter: Optional filter formula
            max_records: Maximum number of records to retrieve (None = all)

        Returns:
            List of all records or None if error
        """
        all_records = []
        page_token = None
        has_more = True

        while has_more:
            result = self.get_base_records(
                app_token=app_token,
                table_id=table_id,
                page_size=500,  # Max per request
                page_token=page_token,
                view_id=view_id,
                filter=filter,
            )

            if not result:
                logger.error("Failed to retrieve records")
                return None

            all_records.extend(result["items"])
            has_more = result["has_more"]
            page_token = result.get("page_token")

            # Check if we've hit max_records limit
            if max_records and len(all_records) >= max_records:
                all_records = all_records[:max_records]
                break

            # Safety check to prevent infinite loops
            if len(all_records) > 10000:
                logger.warning(f"Retrieved over 10,000 records, stopping pagination")
                break

        logger.info(f"Retrieved total of {len(all_records)} records")
        return all_records

    def search_base_records(
        self,
        app_token: str,
        table_id: str,
        filter: Optional[str] = None,
        sort: Optional[List[Dict]] = None,
        field_names: Optional[List[str]] = None,
        page_size: int = 100,
    ) -> Optional[List[Dict]]:
        """
        Search records in a Lark Base table with advanced filtering

        Args:
            app_token: The Base app token
            table_id: The table ID
            filter: Filter formula (e.g., 'CurrentValue.[Field] = "value"')
            sort: List of sort conditions [{"field_name": "Field", "desc": False}]
            field_names: List of field names to return (None = all fields)
            page_size: Number of records per page

        Returns:
            List of matching records or None if error
        """
        if not self.access_token:
            logger.error("Lark client not initialized")
            return None

        self._refresh_token_if_needed()

        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search"

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "page_size": min(page_size, 500)
        }

        if filter:
            payload["filter"] = filter
        if sort:
            payload["sort"] = sort
        if field_names:
            payload["field_names"] = field_names

        try:
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()

            if result.get("code") == 0:
                records = result.get("data", {}).get("items", [])
                logger.info(f"Found {len(records)} matching records")
                return records
            else:
                logger.error(f"Error searching records: {result}")
                return None

        except Exception as e:
            logger.error(f"Error searching base records: {e}")
            return None

    def parse_base_url(self, url: str) -> Optional[Dict[str, str]]:
        """
        Parse a Lark Base URL to extract app_token, table_id, and view_id

        Args:
            url: Lark Base URL (e.g., https://xxx.larksuite.com/base/APP_TOKEN?table=TABLE_ID&view=VIEW_ID)

        Returns:
            Dict with 'app_token', 'table_id', 'view_id' or None if invalid
        """
        import re
        from urllib.parse import urlparse, parse_qs

        try:
            # Extract app_token from path
            match = re.search(r'/base/([a-zA-Z0-9]+)', url)
            if not match:
                logger.error("Could not extract app_token from URL")
                return None

            app_token = match.group(1)

            # Parse query parameters for table_id and view_id
            parsed = urlparse(url)
            params = parse_qs(parsed.query)

            table_id = params.get('table', [None])[0]
            view_id = params.get('view', [None])[0]

            result = {
                'app_token': app_token,
                'table_id': table_id,
                'view_id': view_id
            }

            logger.info(f"Parsed Base URL: {result}")
            return result

        except Exception as e:
            logger.error(f"Error parsing Base URL: {e}")
            return None


# Global Lark client instance
lark_client = LarkClient()


if __name__ == "__main__":
    # Test Lark client
    print("Testing Lark Client...")
    print("=" * 50)

    # Test sending a simple message
    test_message = """
**Daily Plan Test** 📋

Your top 3 priorities today:
1. Complete PRD for Feature X
2. Review design mockups
3. Team standup at 10 AM

Have a productive day! 🚀
"""

    try:
        if settings.dry_run:
            print("Running in DRY RUN mode - no actual messages will be sent")

        result = lark_client.send_daily_plan(test_message)

        if result:
            print("✅ Test message sent successfully")
        else:
            print("⚠️  Test ran but message not sent (check dry run mode)")

    except Exception as e:
        print(f"❌ Test failed: {e}")

    print("\n" + "=" * 50)
