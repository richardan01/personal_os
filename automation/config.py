"""
Personal OS - Configuration Management
Loads environment variables and provides configuration to all agents
"""

import os
from pathlib import Path
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Central configuration for Personal OS"""

    # Base paths
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent)

    # AI Provider Configuration
    ai_provider: str = Field(default="anthropic", description="anthropic or openai")
    ai_model: str = Field(default="claude-sonnet-4-5-20250929")
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    # Slack Configuration
    slack_bot_token: Optional[str] = None
    slack_app_token: Optional[str] = None
    slack_signing_secret: Optional[str] = None
    slack_user_id: Optional[str] = None
    slack_channel_daily: str = "#personal-os-updates"
    slack_channel_weekly: str = "#weekly-summary"

    # Lark Configuration
    lark_app_id: Optional[str] = None
    lark_app_secret: Optional[str] = None
    lark_user_id: Optional[str] = None
    lark_chat_id: Optional[str] = None

    # Messaging Platform Preference
    messaging_platform: str = Field(default="slack", description="slack, lark, or both")

    # Calendar Configuration
    google_calendar_credentials: str = "credentials/google_calendar_credentials.json"
    google_calendar_id: Optional[str] = None

    # Task Management Configuration
    task_system: str = Field(default="notion", description="notion, jira, asana, or linear")

    # Notion
    notion_api_key: Optional[str] = None
    notion_database_id: Optional[str] = None

    # Jira
    jira_url: Optional[str] = None
    jira_email: Optional[str] = None
    jira_api_token: Optional[str] = None
    jira_project_key: Optional[str] = None

    # Asana
    asana_access_token: Optional[str] = None
    asana_workspace_id: Optional[str] = None

    # Linear
    linear_api_key: Optional[str] = None
    linear_team_id: Optional[str] = None

    # Agent Configuration
    timezone: str = "America/New_York"
    execution_agent_morning_time: str = "08:00"
    execution_agent_midday_time: str = "12:30"
    execution_agent_evening_time: str = "17:30"
    strategy_agent_morning_time: str = "08:00"
    strategy_agent_weekly_time: str = "Monday 09:00"
    stakeholder_agent_weekly_update_time: str = "Friday 15:00"
    discovery_agent_daily_digest_time: str = "17:00"

    # Personal Context
    user_name: str = "User"
    user_role: str = "Product Manager"
    company_name: str = "Company"
    current_okrs: str = ""
    strategic_priorities: str = ""

    # Database
    database_url: str = "sqlite:///personal_os.db"

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/personal_os.log"

    # Agent Toggles
    enable_execution_agent: bool = True
    enable_strategy_agent: bool = True
    enable_discovery_agent: bool = True
    enable_stakeholder_agent: bool = True

    # Dry Run
    dry_run: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def okrs_list(self) -> List[str]:
        """Parse OKRs from comma-separated string"""
        if not self.current_okrs:
            return []
        return [okr.strip() for okr in self.current_okrs.split(",")]

    @property
    def priorities_list(self) -> List[str]:
        """Parse strategic priorities from comma-separated string"""
        if not self.strategic_priorities:
            return []
        return [p.strip() for p in self.strategic_priorities.split(",")]

    def validate_slack_config(self) -> bool:
        """Check if Slack is properly configured"""
        return bool(self.slack_bot_token and self.slack_user_id)

    def validate_lark_config(self) -> bool:
        """Check if Lark is properly configured"""
        return bool(self.lark_app_id and self.lark_app_secret and self.lark_user_id)

    def validate_messaging_config(self) -> bool:
        """Check if at least one messaging platform is configured"""
        if self.messaging_platform == "slack":
            return self.validate_slack_config()
        elif self.messaging_platform == "lark":
            return self.validate_lark_config()
        elif self.messaging_platform == "both":
            return self.validate_slack_config() or self.validate_lark_config()
        return False

    def validate_ai_config(self) -> bool:
        """Check if AI provider is properly configured"""
        if self.ai_provider == "anthropic":
            return bool(self.anthropic_api_key)
        elif self.ai_provider == "openai":
            return bool(self.openai_api_key)
        return False

    def validate_task_system_config(self) -> bool:
        """Check if task management system is properly configured"""
        if self.task_system == "notion":
            return bool(self.notion_api_key and self.notion_database_id)
        elif self.task_system == "jira":
            return bool(self.jira_url and self.jira_email and self.jira_api_token)
        elif self.task_system == "asana":
            return bool(self.asana_access_token and self.asana_workspace_id)
        elif self.task_system == "linear":
            return bool(self.linear_api_key and self.linear_team_id)
        return False


# Global settings instance
settings = Settings()


def validate_configuration():
    """Validate that all required configuration is present"""
    errors = []
    warnings = []

    if not settings.validate_ai_config():
        errors.append(f"AI provider '{settings.ai_provider}' is not properly configured")

    if not settings.validate_messaging_config():
        errors.append(f"Messaging platform '{settings.messaging_platform}' is not properly configured")

    # Warnings for optional configurations
    if settings.messaging_platform in ["slack", "both"] and not settings.validate_slack_config():
        warnings.append("Slack configuration incomplete - Slack messaging will be disabled")

    if settings.messaging_platform in ["lark", "both"] and not settings.validate_lark_config():
        warnings.append("Lark configuration incomplete - Lark messaging will be disabled")

    if not settings.validate_task_system_config():
        warnings.append(f"Task system '{settings.task_system}' is not properly configured - using placeholder data")

    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  ❌ {error}")
        return False

    if warnings:
        print("\nConfiguration Warnings:")
        for warning in warnings:
            print(f"  ⚠️  {warning}")

    print("\n✅ Configuration validated successfully")
    return True


if __name__ == "__main__":
    # Test configuration
    print("Personal OS Configuration")
    print("=" * 50)
    print(f"AI Provider: {settings.ai_provider}")
    print(f"AI Model: {settings.ai_model}")
    print(f"Task System: {settings.task_system}")
    print(f"Timezone: {settings.timezone}")
    print(f"User: {settings.user_name} ({settings.user_role})")
    print(f"Dry Run: {settings.dry_run}")
    print("\nEnabled Agents:")
    print(f"  - Execution: {settings.enable_execution_agent}")
    print(f"  - Strategy: {settings.enable_strategy_agent}")
    print(f"  - Discovery: {settings.enable_discovery_agent}")
    print(f"  - Stakeholder: {settings.enable_stakeholder_agent}")
    print("\n" + "=" * 50)
    validate_configuration()
