"""
Personal OS Agents
All agent modules for the Personal OS automation system
"""

from .base_agent import BaseAgent, PlaceholderAgent
from .execution_agent import execution_agent, ExecutionAgent
from .strategy_agent import strategy_agent, StrategyAgent
from .discovery_agent import discovery_agent, DiscoveryAgent
from .planning_agent import planning_agent, PlanningAgent
from .stakeholder_agent import stakeholder_agent, StakeholderAgent
from .analytics_agent import analytics_agent, AnalyticsAgent

__all__ = [
    # Base classes
    "BaseAgent",
    "PlaceholderAgent",
    # Agent classes
    "ExecutionAgent",
    "StrategyAgent",
    "DiscoveryAgent",
    "PlanningAgent",
    "StakeholderAgent",
    "AnalyticsAgent",
    # Global instances
    "execution_agent",
    "strategy_agent",
    "discovery_agent",
    "planning_agent",
    "stakeholder_agent",
    "analytics_agent",
]
