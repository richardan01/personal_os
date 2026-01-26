"""
Note Synthesis Skill - AI-powered extraction of insights from notes
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import json
from loguru import logger

from utils.ai_client import ai_client
from models.document import DocumentContent
from models.stakeholder import StakeholderInsight
from models.insight import Concern, Need, Quote, MentionedStakeholder
from models.action import ActionItem
from models.enums import (
    Sentiment,
    Severity,
    Priority,
    ConcernCategory,
    NeedCategory,
)


class NoteSynthesis:
    """
    Skill for AI-powered extraction of insights from meeting notes.

    Uses Claude to:
    - Extract stakeholder information
    - Identify concerns and needs
    - Capture key quotes
    - Extract action items
    - Analyze sentiment
    """

    EXTRACTION_PROMPT = """You are an expert at analyzing meeting notes and extracting stakeholder insights for product management.

Analyze the following meeting notes and extract structured information.

MEETING NOTES:
{content}

DOCUMENT TITLE: {title}
DOCUMENT DATE: {date}

Extract the following information in JSON format:

```json
{{
    "stakeholder": {{
        "name": "Full name of the primary stakeholder",
        "role": "Their job title/role",
        "department": "Their department/team",
        "email": "Email if mentioned, otherwise empty string"
    }},
    "meeting_type": "interview|workshop|1:1|group|other",
    "concerns": [
        {{
            "description": "Description of the concern",
            "category": "budget|timeline|resource|technical|political|change_management|risk|other",
            "severity": "high|medium|low",
            "quote": "Direct quote if available, otherwise null"
        }}
    ],
    "needs": [
        {{
            "description": "Description of the need",
            "category": "functional|information|process|communication|support|recognition",
            "priority": "must_have|should_have|nice_to_have",
            "quote": "Direct quote if available, otherwise null"
        }}
    ],
    "goals": ["List of stakeholder's goals/objectives mentioned"],
    "constraints": ["List of limitations or constraints they face"],
    "key_quotes": [
        {{
            "text": "The exact quote",
            "context": "What prompted this statement",
            "topic": "What topic this relates to",
            "sentiment": "positive|neutral|negative|mixed",
            "is_highlight": true/false
        }}
    ],
    "mentioned_stakeholders": [
        {{
            "name": "Name of mentioned person",
            "context": "Why they were mentioned",
            "relationship_hint": "e.g., 'works closely with', 'reports to'"
        }}
    ],
    "action_items": [
        {{
            "title": "Action item title",
            "description": "More details",
            "owner": "Who should do this",
            "due_date": "YYYY-MM-DD if mentioned, otherwise null",
            "priority": "must_have|should_have|nice_to_have"
        }}
    ],
    "overall_sentiment": "positive|neutral|negative|mixed",
    "sentiment_details": "Brief explanation of the overall sentiment",
    "extraction_confidence": 0.0-1.0
}}
```

Guidelines:
- Be precise and extract only what's explicitly stated or clearly implied
- Use null for fields where information is not available
- Identify the PRIMARY stakeholder (the main person being interviewed/discussed)
- Capture direct quotes when possible - they are valuable evidence
- Rate extraction_confidence based on how clear and complete the notes are
- For concerns and needs, categorize appropriately based on content
- Mark quotes as is_highlight=true if they are particularly insightful or important

Return ONLY the JSON, no other text."""

    def __init__(self):
        self.ai = ai_client

    def extract_stakeholder_insights(
        self,
        document: DocumentContent,
        additional_context: Optional[str] = None,
    ) -> StakeholderInsight:
        """
        Extract stakeholder insights from a document.

        Args:
            document: The document to analyze
            additional_context: Optional additional context

        Returns:
            StakeholderInsight object
        """
        logger.info(f"Extracting insights from: {document.title}")

        # Format the date
        date_str = ""
        if document.modified_at:
            date_str = document.modified_at.strftime("%Y-%m-%d")
        elif document.created_at:
            date_str = document.created_at.strftime("%Y-%m-%d")

        # Build prompt
        prompt = self.EXTRACTION_PROMPT.format(
            content=document.content[:15000],  # Limit content length
            title=document.title,
            date=date_str or "Unknown",
        )

        if additional_context:
            prompt += f"\n\nAdditional Context:\n{additional_context}"

        # Call AI
        response = self.ai.generate(
            prompt=prompt,
            system_prompt="You are a stakeholder research analyst. Extract information precisely and return valid JSON.",
            max_tokens=4000,
            temperature=0.1,  # Low temperature for consistent extraction
        )

        # Parse response
        try:
            # Extract JSON from response
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            return self._build_insight(data, document)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            # Return minimal insight
            return StakeholderInsight(
                source_doc_id=document.id,
                source_doc_title=document.title,
                extraction_confidence=0.0,
                extracted_at=datetime.utcnow(),
            )

    def _build_insight(
        self,
        data: Dict[str, Any],
        document: DocumentContent,
    ) -> StakeholderInsight:
        """Build StakeholderInsight from extracted data"""

        # Parse stakeholder info
        stakeholder = data.get("stakeholder", {})

        # Parse concerns
        concerns = []
        for c in data.get("concerns", []):
            try:
                concerns.append(Concern(
                    description=c.get("description", ""),
                    category=ConcernCategory(c.get("category", "other")),
                    severity=Severity(c.get("severity", "medium")),
                    quote=c.get("quote"),
                ))
            except (ValueError, KeyError) as e:
                logger.warning(f"Error parsing concern: {e}")

        # Parse needs
        needs = []
        for n in data.get("needs", []):
            try:
                needs.append(Need(
                    description=n.get("description", ""),
                    category=NeedCategory(n.get("category", "functional")),
                    priority=Priority(n.get("priority", "should_have")),
                    quote=n.get("quote"),
                ))
            except (ValueError, KeyError) as e:
                logger.warning(f"Error parsing need: {e}")

        # Parse quotes
        quotes = []
        for q in data.get("key_quotes", []):
            try:
                quotes.append(Quote(
                    text=q.get("text", ""),
                    context=q.get("context", ""),
                    topic=q.get("topic", ""),
                    sentiment=Sentiment(q.get("sentiment", "neutral")),
                    is_highlight=q.get("is_highlight", False),
                ))
            except (ValueError, KeyError) as e:
                logger.warning(f"Error parsing quote: {e}")

        # Parse mentioned stakeholders
        mentioned = []
        for m in data.get("mentioned_stakeholders", []):
            mentioned.append(MentionedStakeholder(
                name=m.get("name", ""),
                context=m.get("context", ""),
                relationship_hint=m.get("relationship_hint", ""),
            ))

        # Parse action items
        actions = []
        for a in data.get("action_items", []):
            due_date = None
            if a.get("due_date"):
                try:
                    due_date = datetime.strptime(a["due_date"], "%Y-%m-%d")
                except ValueError:
                    pass

            try:
                actions.append(ActionItem(
                    title=a.get("title", ""),
                    description=a.get("description", ""),
                    owner=a.get("owner", ""),
                    stakeholder=stakeholder.get("name", ""),
                    due_date=due_date,
                    priority=Priority(a.get("priority", "should_have")),
                    source_doc_id=document.id,
                    source_meeting_date=document.modified_at,
                ))
            except (ValueError, KeyError) as e:
                logger.warning(f"Error parsing action: {e}")

        # Parse sentiment
        try:
            sentiment = Sentiment(data.get("overall_sentiment", "neutral"))
        except ValueError:
            sentiment = Sentiment.NEUTRAL

        return StakeholderInsight(
            source_doc_id=document.id,
            source_doc_title=document.title,
            meeting_date=document.modified_at or document.created_at,
            meeting_type=data.get("meeting_type", "interview"),
            stakeholder_name=stakeholder.get("name", ""),
            stakeholder_role=stakeholder.get("role", ""),
            stakeholder_department=stakeholder.get("department", ""),
            stakeholder_email=stakeholder.get("email", ""),
            concerns=concerns,
            needs=needs,
            goals=data.get("goals", []),
            constraints=data.get("constraints", []),
            overall_sentiment=sentiment,
            sentiment_details=data.get("sentiment_details", ""),
            key_quotes=quotes,
            mentioned_stakeholders=mentioned,
            action_items=actions,
            extraction_confidence=data.get("extraction_confidence", 0.5),
            extracted_at=datetime.utcnow(),
        )

    def extract_action_items(
        self,
        document: DocumentContent,
    ) -> List[ActionItem]:
        """
        Extract only action items from a document.

        Args:
            document: The document to analyze

        Returns:
            List of ActionItem objects
        """
        insight = self.extract_stakeholder_insights(document)
        return insight.action_items

    def extract_key_quotes(
        self,
        document: DocumentContent,
    ) -> List[Quote]:
        """
        Extract only key quotes from a document.

        Args:
            document: The document to analyze

        Returns:
            List of Quote objects
        """
        insight = self.extract_stakeholder_insights(document)
        return insight.key_quotes

    def batch_extract(
        self,
        documents: List[DocumentContent],
    ) -> List[StakeholderInsight]:
        """
        Extract insights from multiple documents.

        Args:
            documents: List of documents to analyze

        Returns:
            List of StakeholderInsight objects
        """
        logger.info(f"Batch extracting insights from {len(documents)} documents")

        insights = []
        for doc in documents:
            try:
                insight = self.extract_stakeholder_insights(doc)
                insights.append(insight)
            except Exception as e:
                logger.error(f"Error extracting from {doc.title}: {e}")

        logger.info(f"Successfully extracted {len(insights)} insights")
        return insights


# Global instance
note_synthesis = NoteSynthesis()
