"""
Stakeholder Discovery Agent - Gather and synthesize stakeholder research notes

This agent orchestrates the stakeholder discovery workflow:
1. Search for meeting notes and interview transcripts
2. Extract insights from documents
3. Build stakeholder profiles
4. Map relationships and influence
5. Aggregate insights and find patterns
6. Create follow-up tasks
7. Generate discovery reports
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from loguru import logger

from skills.document_search import DocumentSearch
from skills.document_reader import DocumentReader
from skills.note_synthesis import NoteSynthesis
from skills.stakeholder_profiler import StakeholderProfiler
from skills.relationship_mapper import RelationshipMapper
from skills.insight_aggregator import InsightAggregator
from skills.task_creator import TaskCreator
from skills.report_generator import ReportGenerator

from models.document import DocumentContent
from models.stakeholder import StakeholderProfile, StakeholderInsight
from models.relationship import InfluenceMatrix
from models.insight import Theme, Conflict
from models.report import DiscoveryReport, InsightSummary
from models.action import ActionItem

from config import settings


class StakeholderDiscoveryAgent:
    """
    Agent for stakeholder discovery and research synthesis.

    Orchestrates the full workflow from gathering notes to generating reports.
    """

    def __init__(self):
        # Initialize skills
        self.document_search = DocumentSearch()
        self.document_reader = DocumentReader()
        self.note_synthesis = NoteSynthesis()
        self.stakeholder_profiler = StakeholderProfiler()
        self.relationship_mapper = RelationshipMapper()
        self.insight_aggregator = InsightAggregator()
        self.task_creator = TaskCreator()
        self.report_generator = ReportGenerator()

        logger.info("Initialized StakeholderDiscoveryAgent")

    def run_discovery(
        self,
        folder_id: Optional[str] = None,
        keywords: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        report_title: str = "Stakeholder Discovery",
        output_folder_id: Optional[str] = None,
        create_tasks: bool = True,
    ) -> DiscoveryReport:
        """
        Run the full stakeholder discovery workflow.

        Args:
            folder_id: Folder containing discovery notes
            keywords: Optional keywords to filter documents
            date_from: Start date for document search
            date_to: End date for document search
            report_title: Title for the generated report
            output_folder_id: Folder to save report to
            create_tasks: Whether to create follow-up tasks

        Returns:
            DiscoveryReport with all findings
        """
        logger.info(f"Starting stakeholder discovery: {report_title}")

        # Step 1: Find documents
        logger.info("Step 1: Searching for documents...")
        documents = self._gather_documents(
            folder_id=folder_id,
            keywords=keywords,
            date_from=date_from,
            date_to=date_to,
        )
        logger.info(f"Found {len(documents)} documents")

        if not documents:
            logger.warning("No documents found. Creating empty report.")
            return DiscoveryReport(title=report_title)

        # Step 2: Read documents
        logger.info("Step 2: Reading documents...")
        document_contents = self._read_documents(documents)
        logger.info(f"Read {len(document_contents)} documents")

        # Step 3: Extract insights
        logger.info("Step 3: Extracting insights...")
        insights = self._extract_insights(document_contents)
        logger.info(f"Extracted insights from {len(insights)} documents")

        # Step 4: Build profiles
        logger.info("Step 4: Building stakeholder profiles...")
        profiles = self._build_profiles(insights)
        logger.info(f"Built {len(profiles)} stakeholder profiles")

        # Step 5: Map relationships
        logger.info("Step 5: Mapping relationships...")
        influence_matrix = self._map_relationships(profiles)

        # Step 6: Aggregate insights
        logger.info("Step 6: Aggregating insights...")
        themes, conflicts, summary = self._aggregate_insights(profiles, insights)
        logger.info(f"Found {len(themes)} themes, {len(conflicts)} conflicts")

        # Step 7: Create tasks (if enabled)
        action_items = []
        if create_tasks:
            logger.info("Step 7: Creating follow-up tasks...")
            action_items = self._create_tasks(profiles, insights)
            logger.info(f"Created {len(action_items)} tasks")

        # Step 8: Generate report
        logger.info("Step 8: Generating report...")
        report = self._generate_report(
            title=report_title,
            profiles=profiles,
            summary=summary,
            influence_matrix=influence_matrix,
            themes=themes,
            conflicts=conflicts,
            action_items=action_items,
            source_documents=document_contents,
            folder_id=output_folder_id,
        )

        logger.info(f"Discovery complete. Report: {report.google_doc_url or 'Not saved'}")
        return report

    def _gather_documents(
        self,
        folder_id: Optional[str] = None,
        keywords: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ) -> List[Dict[str, Any]]:
        """Gather relevant documents from Google Drive"""

        if folder_id:
            # Get all documents from folder
            docs = self.document_search.get_folder_contents(
                folder_id=folder_id,
                recursive=True,
                file_types=["docs", "sheets"],
            )
        elif keywords:
            # Search by keywords
            docs = self.document_search.search(
                keywords=keywords,
                file_types=["docs"],
                date_from=date_from,
                date_to=date_to,
            )
        else:
            # Get recent meeting notes
            docs = self.document_search.find_meeting_notes(
                date_from=date_from or (datetime.utcnow() - timedelta(days=30)),
                date_to=date_to,
            )

        return docs

    def _read_documents(
        self,
        documents: List[Dict[str, Any]],
    ) -> List[DocumentContent]:
        """Read and parse document contents"""

        doc_ids = [d["id"] for d in documents]
        return self.document_reader.read_multiple(doc_ids)

    def _extract_insights(
        self,
        documents: List[DocumentContent],
    ) -> List[StakeholderInsight]:
        """Extract stakeholder insights from documents"""

        return self.note_synthesis.batch_extract(documents)

    def _build_profiles(
        self,
        insights: List[StakeholderInsight],
    ) -> List[StakeholderProfile]:
        """Build stakeholder profiles from insights"""

        return self.stakeholder_profiler.build_profiles_from_insights(
            insights,
            analyze=True,
        )

    def _map_relationships(
        self,
        profiles: List[StakeholderProfile],
    ) -> InfluenceMatrix:
        """Map relationships and build influence matrix"""

        # Build influence matrix
        matrix = self.relationship_mapper.build_influence_matrix(profiles)

        # Identify clusters
        clusters = self.relationship_mapper.identify_clusters(profiles)
        matrix.clusters = clusters

        return matrix

    def _aggregate_insights(
        self,
        profiles: List[StakeholderProfile],
        insights: List[StakeholderInsight],
    ) -> tuple:
        """Aggregate insights to find patterns"""

        # Find themes
        themes = self.insight_aggregator.find_common_themes(profiles)

        # Find conflicts
        conflicts = self.insight_aggregator.find_conflicts(profiles)

        # Generate summary
        summary = self.insight_aggregator.generate_summary(profiles, insights)

        return themes, conflicts, summary

    def _create_tasks(
        self,
        profiles: List[StakeholderProfile],
        insights: List[StakeholderInsight],
    ) -> List[ActionItem]:
        """Create follow-up tasks from action items"""

        # Collect all action items
        all_actions = []
        for insight in insights:
            all_actions.extend(insight.action_items)

        # Create tasks in Google Tasks
        updated_actions = self.task_creator.batch_create(all_actions)

        # Also create follow-up tasks for key stakeholders
        for profile in profiles:
            if profile.stance in ["blocker", "skeptic"]:
                # Create follow-up for skeptics/blockers
                self.task_creator.create_follow_up(
                    stakeholder=profile.name,
                    topic="Address concerns and build alignment",
                    due_date=datetime.utcnow() + timedelta(days=7),
                    notes=f"Key concerns: {', '.join(c.description for c in profile.top_concerns[:3])}",
                )

        return updated_actions

    def _generate_report(
        self,
        title: str,
        profiles: List[StakeholderProfile],
        summary: InsightSummary,
        influence_matrix: InfluenceMatrix,
        themes: List[Theme],
        conflicts: List[Conflict],
        action_items: List[ActionItem],
        source_documents: List[DocumentContent],
        folder_id: Optional[str] = None,
    ) -> DiscoveryReport:
        """Generate the final discovery report"""

        report = self.report_generator.generate_discovery_report(
            title=title,
            profiles=profiles,
            insight_summary=summary,
            influence_matrix=influence_matrix,
            themes=themes,
            conflicts=conflicts,
            folder_id=folder_id,
        )

        report.action_plan = action_items
        report.source_documents = source_documents

        return report

    # === Convenience Methods ===

    def analyze_folder(
        self,
        folder_id: str,
        report_title: Optional[str] = None,
    ) -> DiscoveryReport:
        """
        Analyze all documents in a folder.

        Args:
            folder_id: Google Drive folder ID
            report_title: Optional report title

        Returns:
            DiscoveryReport
        """
        title = report_title or f"Discovery Report - {datetime.utcnow().strftime('%Y-%m-%d')}"
        return self.run_discovery(folder_id=folder_id, report_title=title)

    def analyze_recent_notes(
        self,
        days: int = 30,
        report_title: Optional[str] = None,
    ) -> DiscoveryReport:
        """
        Analyze recent meeting notes.

        Args:
            days: Number of days to look back
            report_title: Optional report title

        Returns:
            DiscoveryReport
        """
        title = report_title or f"Recent Discovery - {datetime.utcnow().strftime('%Y-%m-%d')}"
        return self.run_discovery(
            date_from=datetime.utcnow() - timedelta(days=days),
            report_title=title,
        )

    def get_stakeholder_summary(
        self,
        stakeholder_name: str,
    ) -> Optional[StakeholderProfile]:
        """
        Get summary for a specific stakeholder.

        Args:
            stakeholder_name: Name of the stakeholder

        Returns:
            StakeholderProfile or None
        """
        # Search for documents mentioning this stakeholder
        docs = self.document_search.search_by_stakeholder(stakeholder_name)

        if not docs:
            logger.warning(f"No documents found for {stakeholder_name}")
            return None

        # Read and extract
        contents = self.document_reader.read_multiple([d["id"] for d in docs])
        insights = self.note_synthesis.batch_extract(contents)

        # Filter insights for this stakeholder
        relevant_insights = [
            i for i in insights
            if i.stakeholder_name.lower() == stakeholder_name.lower()
        ]

        if not relevant_insights:
            logger.warning(f"No insights found for {stakeholder_name}")
            return None

        # Build profile
        profile = self.stakeholder_profiler.get_or_create_profile(stakeholder_name)
        for insight in relevant_insights:
            self.stakeholder_profiler.update_from_insight(profile, insight)

        self.stakeholder_profiler.analyze_profile(profile)

        return profile

    def get_all_profiles(self) -> List[StakeholderProfile]:
        """
        Get all current stakeholder profiles.

        Returns:
            List of StakeholderProfile objects
        """
        return self.stakeholder_profiler.list_all_profiles()

    def export_data(self) -> Dict[str, Any]:
        """
        Export all discovery data.

        Returns:
            Dict containing all profiles and data
        """
        profiles = self.stakeholder_profiler.export_profiles()
        return {
            "profiles": profiles,
            "exported_at": datetime.utcnow().isoformat(),
            "total_stakeholders": len(profiles),
        }


# Global agent instance
stakeholder_discovery_agent = StakeholderDiscoveryAgent()


if __name__ == "__main__":
    # Test the agent
    print("Testing Stakeholder Discovery Agent...")
    print("=" * 50)

    if settings.dry_run:
        print("Running in DRY RUN mode")

    # Run a simple discovery
    # report = stakeholder_discovery_agent.analyze_recent_notes(days=7)
    # print(f"Report generated: {report.title}")

    print("\nAgent ready for use.")
    print("=" * 50)
