"""
Slack Client - Send messages and interact with Slack
"""

from typing import Optional, List, Dict, Any
from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import settings


class SlackClient:
    """Client for sending messages to Slack"""

    def __init__(self):
        if not settings.slack_bot_token:
            logger.warning("Slack bot token not configured")
            self.client = None
        else:
            self.client = WebClient(token=settings.slack_bot_token)
            logger.info("Initialized Slack client")

    def send_message(
        self,
        text: str,
        channel: Optional[str] = None,
        blocks: Optional[List[Dict]] = None,
        thread_ts: Optional[str] = None,
    ) -> Optional[Dict]:
        """
        Send a message to Slack

        Args:
            text: Message text (markdown supported)
            channel: Channel ID or name (e.g., #general or @username)
                    If None, sends to user configured in settings
            blocks: Optional Slack blocks for rich formatting
            thread_ts: Optional thread timestamp to reply in thread

        Returns:
            Response from Slack API or None if dry run
        """
        if settings.dry_run:
            logger.info(f"[DRY RUN] Would send to {channel or settings.slack_user_id}: {text[:100]}...")
            return None

        if not self.client:
            logger.error("Slack client not initialized - check your configuration")
            return None

        # Default to sending DM to configured user
        target = channel or settings.slack_user_id

        try:
            kwargs = {
                "channel": target,
                "text": text,
            }

            if blocks:
                kwargs["blocks"] = blocks

            if thread_ts:
                kwargs["thread_ts"] = thread_ts

            response = self.client.chat_postMessage(**kwargs)
            logger.info(f"Sent message to {target}")
            return response

        except SlackApiError as e:
            logger.error(f"Slack API error: {e.response['error']}")
            return None

    def send_dm(self, text: str, user_id: Optional[str] = None, **kwargs) -> Optional[Dict]:
        """
        Send a direct message to a user

        Args:
            text: Message text
            user_id: User ID to send to (defaults to configured user)
            **kwargs: Additional arguments for send_message

        Returns:
            Response from Slack API or None
        """
        target_user = user_id or settings.slack_user_id
        return self.send_message(text, channel=target_user, **kwargs)

    def send_formatted_message(
        self,
        title: str,
        body: str,
        channel: Optional[str] = None,
        fields: Optional[List[Dict[str, str]]] = None,
        color: str = "#36a64f",
    ) -> Optional[Dict]:
        """
        Send a formatted message with attachment/blocks

        Args:
            title: Message title
            body: Message body
            channel: Channel to send to
            fields: Optional list of {title, value, short} dicts
            color: Color bar for attachment (hex color)

        Returns:
            Response from Slack API or None
        """
        # Create blocks for better formatting
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title,
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": body,
                }
            }
        ]

        # Add fields if provided
        if fields:
            fields_block = {
                "type": "section",
                "fields": []
            }
            for field in fields:
                fields_block["fields"].append({
                    "type": "mrkdwn",
                    "text": f"*{field['title']}*\n{field['value']}"
                })
            blocks.append(fields_block)

        return self.send_message("", channel=channel, blocks=blocks)

    def send_daily_plan(self, plan: str, channel: Optional[str] = None) -> Optional[Dict]:
        """
        Send daily plan in a nice format

        Args:
            plan: The daily plan text
            channel: Channel to send to (defaults to daily channel)

        Returns:
            Response from Slack API or None
        """
        target = channel or settings.slack_channel_daily

        return self.send_formatted_message(
            title="📋 Your Daily Plan",
            body=plan,
            channel=target,
            color="#2eb886"
        )

    def send_status_update(self, update: str, channel: Optional[str] = None) -> Optional[Dict]:
        """
        Send a status update

        Args:
            update: Status update text
            channel: Channel to send to (defaults to weekly channel)

        Returns:
            Response from Slack API or None
        """
        target = channel or settings.slack_channel_weekly

        return self.send_formatted_message(
            title="📊 Status Update",
            body=update,
            channel=target,
            color="#3b88c3"
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
            Response from Slack API or None
        """
        colors = {
            "info": "#36a64f",
            "warning": "#ff9900",
            "error": "#ff0000"
        }

        emoji = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "🚨"
        }

        return self.send_formatted_message(
            title=f"{emoji.get(severity, '📢')} {title}",
            body=message,
            channel=settings.slack_user_id,
            color=colors.get(severity, "#36a64f")
        )

    def get_user_info(self, user_id: Optional[str] = None) -> Optional[Dict]:
        """Get information about a Slack user"""
        if not self.client:
            return None

        try:
            target_user = user_id or settings.slack_user_id
            response = self.client.users_info(user=target_user)
            return response["user"]
        except SlackApiError as e:
            logger.error(f"Error getting user info: {e}")
            return None


# Global Slack client instance
slack_client = SlackClient()


if __name__ == "__main__":
    # Test Slack client
    print("Testing Slack Client...")
    print("=" * 50)

    # Test sending a simple message
    test_message = """
*Daily Plan Test* 📋

Your top 3 priorities today:
1. Complete PRD for Feature X
2. Review design mockups
3. Team standup at 10 AM

Have a productive day! 🚀
"""

    try:
        if settings.dry_run:
            print("Running in DRY RUN mode - no actual messages will be sent")

        result = slack_client.send_dm(test_message)

        if result:
            print("✅ Test message sent successfully")
        else:
            print("⚠️  Test ran but message not sent (check dry run mode)")

    except Exception as e:
        print(f"❌ Test failed: {e}")

    print("\n" + "=" * 50)
