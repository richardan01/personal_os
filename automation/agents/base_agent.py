"""
Base Agent - Foundation for all Personal OS agents
Provides common functionality and interface for agent implementations
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime, date
from loguru import logger

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from utils.ai_client import ai_client
from utils.messaging_client import messaging_client


class BaseAgent(ABC):
    """Abstract base class for all Personal OS agents"""

    def __init__(self, name: str, emoji: str = "🤖"):
        self.name = name
        self.emoji = emoji
        self.user_name = settings.user_name
        self.user_role = settings.user_role
        self.company_name = settings.company_name
        logger.info(f"Initialized {self.name}")

    @property
    def current_date(self) -> str:
        """Get current date formatted"""
        return date.today().strftime("%Y-%m-%d")

    @property
    def current_time(self) -> str:
        """Get current time formatted"""
        return datetime.now().strftime("%I:%M %p")

    @property
    def day_of_week(self) -> str:
        """Get current day of week"""
        return date.today().strftime("%A")

    @property
    def strategic_priorities(self) -> List[str]:
        """Get strategic priorities from config"""
        return settings.priorities_list

    @property
    def okrs(self) -> List[str]:
        """Get OKRs from config"""
        return settings.okrs_list

    def generate_ai_response(
        self,
        prompt: str,
        system_prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7
    ) -> str:
        """
        Generate AI response using configured AI client

        Args:
            prompt: The user prompt
            system_prompt: System context for the AI
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0-1)

        Returns:
            Generated response text
        """
        try:
            response = ai_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response
        except Exception as e:
            logger.error(f"Error generating AI response in {self.name}: {e}")
            raise

    def send_to_messaging(self, message: str, title: Optional[str] = None) -> None:
        """
        Send message to configured messaging platform

        Args:
            message: The message content
            title: Optional title/header for the message
        """
        try:
            formatted_message = f"{self.emoji} *{title or self.name}*\n\n{message}"
            messaging_client.send_dm(formatted_message)
            logger.info(f"{self.name} sent message to messaging platform")
        except Exception as e:
            logger.error(f"Error sending message from {self.name}: {e}")

    def send_alert(self, title: str, message: str, severity: str = "warning") -> None:
        """
        Send alert to messaging platform

        Args:
            title: Alert title
            message: Alert message
            severity: Alert level (info, warning, error)
        """
        try:
            messaging_client.send_alert(
                title=f"{self.emoji} {title}",
                message=message,
                severity=severity
            )
            logger.info(f"{self.name} sent {severity} alert: {title}")
        except Exception as e:
            logger.error(f"Error sending alert from {self.name}: {e}")

    def format_list(self, items: List[str], bullet: str = "-") -> str:
        """Format a list of items with bullets"""
        if not items:
            return f"{bullet} None"
        return "\n".join(f"{bullet} {item}" for item in items)

    def format_dict_list(
        self,
        items: List[Dict[str, Any]],
        template: str,
        keys: List[str]
    ) -> str:
        """
        Format a list of dicts using a template

        Args:
            items: List of dictionaries
            template: Format string with {key} placeholders
            keys: Keys to extract from each dict

        Returns:
            Formatted string
        """
        if not items:
            return "- None"

        formatted = []
        for item in items:
            values = {k: item.get(k, "N/A") for k in keys}
            formatted.append(template.format(**values))

        return "\n".join(formatted)

    @abstractmethod
    def run_workflow(self, **kwargs) -> str:
        """
        Main workflow method - must be implemented by each agent

        Returns:
            Workflow output as string
        """
        pass


class PlaceholderAgent(BaseAgent):
    """
    Placeholder agent for features not yet implemented
    Provides friendly "coming soon" responses
    """

    def __init__(self, name: str, emoji: str = "🚧"):
        super().__init__(name, emoji)

    def run_workflow(self, **kwargs) -> str:
        """Return a placeholder message"""
        message = f"""
{self.emoji} **{self.name} - Coming Soon!**

This agent is currently under development.

**Planned Capabilities:**
- Automated workflows
- AI-powered insights
- Scheduled triggers

Stay tuned for updates!
"""
        return message

    def send_placeholder_message(self) -> None:
        """Send placeholder notification"""
        self.send_to_messaging(
            self.run_workflow(),
            title=f"{self.name} Update"
        )
