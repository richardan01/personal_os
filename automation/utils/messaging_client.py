"""
Unified Messaging Client - Sends messages to Slack and/or Lark
"""

from typing import Optional
from loguru import logger
from config import settings


class MessagingClient:
    """Unified client for sending messages to configured platforms"""

    def __init__(self):
        self.platform = settings.messaging_platform
        self.slack_client = None
        self.lark_client = None

        # Initialize clients based on configuration
        if self.platform in ["slack", "both"]:
            try:
                from utils.slack_client import slack_client
                self.slack_client = slack_client
                logger.info("Slack client initialized")
            except Exception as e:
                logger.warning(f"Could not initialize Slack client: {e}")

        if self.platform in ["lark", "both"]:
            try:
                from utils.lark_client import lark_client
                self.lark_client = lark_client
                logger.info("Lark client initialized")
            except Exception as e:
                logger.warning(f"Could not initialize Lark client: {e}")

    def send_message(self, text: str, channel: Optional[str] = None) -> bool:
        """
        Send a message to all configured platforms

        Args:
            text: Message text
            channel: Optional channel/user to send to

        Returns:
            True if at least one platform succeeded
        """
        success = False

        if self.slack_client and self.platform in ["slack", "both"]:
            try:
                result = self.slack_client.send_message(text, channel=channel)
                if result:
                    success = True
                    logger.info("Message sent to Slack")
            except Exception as e:
                logger.error(f"Failed to send to Slack: {e}")

        if self.lark_client and self.platform in ["lark", "both"]:
            try:
                result = self.lark_client.send_message(text, receive_id=channel)
                if result:
                    success = True
                    logger.info("Message sent to Lark")
            except Exception as e:
                logger.error(f"Failed to send to Lark: {e}")

        return success

    def send_dm(self, text: str) -> bool:
        """Send a direct message to configured user on all platforms"""
        success = False

        if self.slack_client and self.platform in ["slack", "both"]:
            try:
                result = self.slack_client.send_dm(text)
                if result:
                    success = True
            except Exception as e:
                logger.error(f"Failed to send DM to Slack: {e}")

        if self.lark_client and self.platform in ["lark", "both"]:
            try:
                result = self.lark_client.send_dm(text)
                if result:
                    success = True
            except Exception as e:
                logger.error(f"Failed to send DM to Lark: {e}")

        return success

    def send_daily_plan(self, plan: str) -> bool:
        """Send daily plan to all configured platforms"""
        success = False

        if self.slack_client and self.platform in ["slack", "both"]:
            try:
                result = self.slack_client.send_daily_plan(plan)
                if result:
                    success = True
            except Exception as e:
                logger.error(f"Failed to send daily plan to Slack: {e}")

        if self.lark_client and self.platform in ["lark", "both"]:
            try:
                result = self.lark_client.send_daily_plan(plan)
                if result:
                    success = True
            except Exception as e:
                logger.error(f"Failed to send daily plan to Lark: {e}")

        return success

    def send_status_update(self, update: str) -> bool:
        """Send status update to all configured platforms"""
        success = False

        if self.slack_client and self.platform in ["slack", "both"]:
            try:
                result = self.slack_client.send_status_update(update)
                if result:
                    success = True
            except Exception as e:
                logger.error(f"Failed to send status update to Slack: {e}")

        if self.lark_client and self.platform in ["lark", "both"]:
            try:
                result = self.lark_client.send_status_update(update)
                if result:
                    success = True
            except Exception as e:
                logger.error(f"Failed to send status update to Lark: {e}")

        return success

    def send_alert(self, title: str, message: str, severity: str = "warning") -> bool:
        """Send an alert to all configured platforms"""
        success = False

        if self.slack_client and self.platform in ["slack", "both"]:
            try:
                result = self.slack_client.send_alert(title, message, severity)
                if result:
                    success = True
            except Exception as e:
                logger.error(f"Failed to send alert to Slack: {e}")

        if self.lark_client and self.platform in ["lark", "both"]:
            try:
                result = self.lark_client.send_alert(title, message, severity)
                if result:
                    success = True
            except Exception as e:
                logger.error(f"Failed to send alert to Lark: {e}")

        return success


# Global messaging client instance
messaging_client = MessagingClient()


if __name__ == "__main__":
    # Test messaging client
    print("Testing Messaging Client...")
    print("=" * 50)
    print(f"Platform: {settings.messaging_platform}")
    print(f"Slack enabled: {messaging_client.slack_client is not None}")
    print(f"Lark enabled: {messaging_client.lark_client is not None}")
    print()

    test_message = "🧪 Test message from Personal OS"

    try:
        success = messaging_client.send_dm(test_message)
        if success:
            print("✅ Test message sent successfully")
        else:
            print("⚠️  No messages sent (check configuration and dry run mode)")
    except Exception as e:
        print(f"❌ Test failed: {e}")

    print("\n" + "=" * 50)
