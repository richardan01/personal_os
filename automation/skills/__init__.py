"""
Skills for Personal OS

Skills are reusable building blocks that agents can compose for workflows.
Each skill is stateless and single-purpose.

Available Skills:
- DocumentSearch: Find documents in Google Drive
- DocumentReader: Extract content from Google Workspace documents
- NoteSynthesis: AI-powered extraction of insights from notes
- StakeholderProfiler: Build and update stakeholder profiles
- RelationshipMapper: Map relationships and influence between stakeholders
- InsightAggregator: Aggregate insights across stakeholders
- TaskCreator: Create tasks in Google Tasks
- ReportGenerator: Generate formatted reports in Google Docs
"""

from skills.document_search import DocumentSearch
from skills.document_reader import DocumentReader
from skills.note_synthesis import NoteSynthesis
from skills.stakeholder_profiler import StakeholderProfiler
from skills.relationship_mapper import RelationshipMapper
from skills.insight_aggregator import InsightAggregator
from skills.task_creator import TaskCreator
from skills.report_generator import ReportGenerator

__all__ = [
    "DocumentSearch",
    "DocumentReader",
    "NoteSynthesis",
    "StakeholderProfiler",
    "RelationshipMapper",
    "InsightAggregator",
    "TaskCreator",
    "ReportGenerator",
]
