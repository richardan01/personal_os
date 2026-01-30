"""
Documentation Agent - Knowledge management and documentation creation

Handles PRD creation, decision logging, meeting notes organization,
and knowledge base management.
"""

from typing import Dict, List, Any, Optional
from loguru import logger
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from utils.messaging_client import messaging_client


class DocumentationAgent(BaseAgent):
    """
    Documentation Agent for knowledge management.

    Capabilities:
    - PRD creation and maintenance
    - Decision log tracking
    - Meeting notes organization
    - Wiki/knowledge base management
    - Process documentation
    """

    def __init__(self):
        super().__init__("Documentation Agent", "📚")

    def run_workflow(self, **kwargs) -> str:
        """
        Main workflow for documentation agent.

        Args:
            workflow_type: Type of documentation workflow to run
            **kwargs: Additional parameters for the workflow

        Returns:
            Generated documentation
        """
        workflow_type = kwargs.get("workflow_type", "general")

        if workflow_type == "prd":
            return self.generate_prd(**kwargs)
        elif workflow_type == "decision_log":
            return self.generate_decision_log(**kwargs)
        elif workflow_type == "meeting_notes":
            return self.organize_meeting_notes(**kwargs)
        else:
            return self._general_documentation(**kwargs)

    def generate_prd(
        self,
        feature_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a Product Requirements Document.

        Args:
            feature_name: Name of the feature
            context: Additional context for the PRD

        Returns:
            Formatted PRD
        """
        logger.info(f"{self.name}: Generating PRD for {feature_name or 'feature'}")

        context = context or {}
        feature_name = feature_name or "New Feature"

        system_prompt = f"""
You are a product manager creating a comprehensive PRD.

User: {self.user_name}
Role: {self.user_role}
Company: {self.company_name}

Current OKRs:
{self.format_list(self.okrs)}

Strategic Priorities:
{self.format_list(self.strategic_priorities)}

Create a clear, structured PRD that includes:
1. Overview and goals
2. User stories
3. Requirements (functional and non-functional)
4. Success metrics
5. Out of scope
6. Open questions
"""

        prompt = f"""
Create a PRD for: {feature_name}

{f"Additional Context: {context.get('description', '')}" if context.get('description') else ''}

Format the PRD with markdown headers and clear sections.
"""

        try:
            prd_content = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=3000,
                temperature=0.7
            )

            # Add metadata header
            prd = f"""# Product Requirements Document: {feature_name}

**Status:** Draft
**Author:** {self.user_name}
**Date:** {self.current_date}
**Last Updated:** {self.current_date}

---

{prd_content}
"""
            return prd

        except Exception as e:
            logger.error(f"Error generating PRD: {e}")
            return f"Error generating PRD: {str(e)}"

    def generate_decision_log(
        self,
        decision: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a decision log entry.

        Args:
            decision: The decision made
            context: Context including alternatives, rationale, etc.

        Returns:
            Formatted decision log entry
        """
        logger.info(f"{self.name}: Generating decision log")

        context = context or {}
        decision = decision or context.get("decision", "Decision")

        system_prompt = f"""
You are documenting an important decision.

User: {self.user_name}
Role: {self.user_role}

Create a decision log entry that includes:
1. Decision statement (what was decided)
2. Context (why this decision was needed)
3. Alternatives considered
4. Rationale (why this option was chosen)
5. Trade-offs
6. Next steps
"""

        prompt = f"""
Decision: {decision}

{f"Context: {context.get('context', '')}" if context.get('context') else ''}
{f"Alternatives: {context.get('alternatives', '')}" if context.get('alternatives') else ''}
{f"Rationale: {context.get('rationale', '')}" if context.get('rationale') else ''}

Create a structured decision log entry.
"""

        try:
            decision_content = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.6
            )

            # Add metadata
            log_entry = f"""## Decision Log Entry - {self.current_date}

**Decision Owner:** {self.user_name}
**Date:** {self.current_date}
**Status:** Approved

---

{decision_content}

---

**Tags:** {', '.join(context.get('tags', ['decision', 'product']))}
"""
            return log_entry

        except Exception as e:
            logger.error(f"Error generating decision log: {e}")
            return f"Error generating decision log: {str(e)}"

    def organize_meeting_notes(
        self,
        meeting_title: Optional[str] = None,
        notes: Optional[str] = None,
        participants: Optional[List[str]] = None
    ) -> str:
        """
        Organize and structure meeting notes.

        Args:
            meeting_title: Title of the meeting
            notes: Raw meeting notes
            participants: List of participants

        Returns:
            Structured meeting notes
        """
        logger.info(f"{self.name}: Organizing meeting notes")

        meeting_title = meeting_title or "Team Meeting"
        notes = notes or "No notes provided"
        participants = participants or [self.user_name]

        system_prompt = """
You are organizing meeting notes into a structured format.

Extract:
1. Key discussion points
2. Decisions made
3. Action items (with owners)
4. Next steps
5. Open questions

Format in clear markdown with headers.
"""

        prompt = f"""
Meeting: {meeting_title}
Date: {self.current_date}
Participants: {', '.join(participants)}

Raw notes:
{notes}

Organize these notes into a structured format.
"""

        try:
            organized_notes = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,
                temperature=0.6
            )

            # Add metadata
            formatted_notes = f"""# Meeting Notes: {meeting_title}

**Date:** {self.current_date}
**Time:** {self.current_time}
**Participants:** {', '.join(participants)}

---

{organized_notes}
"""
            return formatted_notes

        except Exception as e:
            logger.error(f"Error organizing meeting notes: {e}")
            return f"Error organizing meeting notes: {str(e)}"

    def _general_documentation(self, **kwargs) -> str:
        """
        Generate general documentation based on request.

        Returns:
            Documentation content
        """
        doc_type = kwargs.get("doc_type", "general")
        content = kwargs.get("content", "")

        logger.info(f"{self.name}: Generating {doc_type} documentation")

        system_prompt = f"""
You are a technical writer creating clear documentation.

User: {self.user_name}
Role: {self.user_role}

Create well-structured documentation with:
- Clear headers
- Bullet points for lists
- Examples where appropriate
- Searchable keywords
"""

        prompt = f"""
Create documentation for: {doc_type}

{f"Content: {content}" if content else ''}

Format in markdown with clear structure.
"""

        try:
            documentation = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2500,
                temperature=0.7
            )

            return f"""# {doc_type.replace('_', ' ').title()}

**Created:** {self.current_date}
**Author:** {self.user_name}

---

{documentation}
"""

        except Exception as e:
            logger.error(f"Error generating documentation: {e}")
            return f"Error generating documentation: {str(e)}"

    def send_documentation_update(
        self,
        doc_type: str,
        content: str,
        recipients: Optional[List[str]] = None
    ) -> None:
        """
        Send documentation update via messaging.

        Args:
            doc_type: Type of documentation
            content: Documentation content
            recipients: Optional list of recipients
        """
        message = f"""**New Documentation Available**

Type: {doc_type}
Date: {self.current_date}

{content[:500]}...

[View full documentation]
"""
        self.send_to_messaging(message, title=f"Documentation: {doc_type}")


# Global singleton instance
documentation_agent = DocumentationAgent()


if __name__ == "__main__":
    # Test the agent
    print("Testing Documentation Agent...")

    # Test PRD generation
    prd = documentation_agent.generate_prd(
        feature_name="User Authentication",
        context={"description": "Add OAuth login to the application"}
    )
    print("\nGenerated PRD:")
    print(prd[:500])

    # Test decision log
    decision_log = documentation_agent.generate_decision_log(
        decision="Use PostgreSQL for database",
        context={
            "context": "Need to choose database for new application",
            "alternatives": "MongoDB, PostgreSQL, MySQL",
            "rationale": "Need relational data and strong ACID guarantees"
        }
    )
    print("\nGenerated Decision Log:")
    print(decision_log[:500])
