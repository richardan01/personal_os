"""
Analytics Agent - Data-driven decision making
Handles metrics tracking, A/B test analysis, and performance monitoring
"""

from typing import Dict, List, Any, Optional
from loguru import logger

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from agents.base_agent import BaseAgent
from utils.messaging_client import messaging_client


class AnalyticsAgent(BaseAgent):
    """Handles analytics and data-driven insights"""

    def __init__(self):
        super().__init__("Analytics Agent", "📊")

    def run_workflow(self, **kwargs) -> str:
        """Run the analytics workflow"""
        workflow_type = kwargs.get("workflow_type", "metrics_review")

        if workflow_type == "metrics_review":
            return self.generate_metrics_review(
                metrics=kwargs.get("metrics", {})
            )
        elif workflow_type == "ab_test_analysis":
            return self.analyze_ab_test(
                test_name=kwargs.get("test_name", "Unknown Test"),
                results=kwargs.get("results", {})
            )
        else:
            return self.generate_metrics_review()

    def generate_metrics_review(
        self,
        metrics: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a metrics review

        Args:
            metrics: Dictionary of current metrics data

        Returns:
            Metrics review report
        """
        logger.info("Generating metrics review...")

        metrics_text = ""
        if metrics:
            for name, data in metrics.items():
                if isinstance(data, dict):
                    metrics_text += f"- {name}: {data.get('value', 'N/A')} (Target: {data.get('target', 'N/A')}, Trend: {data.get('trend', 'N/A')})\n"
                else:
                    metrics_text += f"- {name}: {data}\n"
        else:
            metrics_text = "No metrics data provided - using placeholders"

        prompt = f"""
ROLE: Product Analytics Expert
CONTEXT: Reviewing metrics for {self.user_name}, {self.user_role}

TODAY: {self.current_date}

CURRENT METRICS:
{metrics_text}

OKRS:
{self.format_list(self.okrs)}

TASK:
Create a metrics review:

## Metrics Review - {self.current_date}

### Key Metrics Snapshot
| Metric | Current | Target | WoW Change | Status |
Assess key product metrics.

### Performance Summary
Overall health: [Healthy / Watch / Alert]

### Trends Analysis
**Improving:**
- [Metric]: [Why it's improving]

**Declining:**
- [Metric]: [Why and what to do]

**Stable:**
- [Metric]: [Is this good or bad?]

### Anomalies Detected
Any unusual patterns or outliers.

### OKR Impact
How do these metrics affect OKR progress?

### Insights
1. [Key insight with recommendation]
2. [Key insight with recommendation]

### Recommended Actions
Specific actions based on the data.

### Data Gaps
What metrics are we missing?

Ground all insights in data. Be specific about numbers.
"""

        system_prompt = f"""You are a product analytics expert helping {self.user_name}
make data-driven decisions. Be rigorous with data interpretation."""

        try:
            review = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1500,
                temperature=0.5
            )
            logger.info("Metrics review generated successfully")
            return review

        except Exception as e:
            logger.error(f"Error generating metrics review: {e}")
            raise

    def analyze_ab_test(
        self,
        test_name: str,
        results: Dict[str, Any]
    ) -> str:
        """
        Analyze A/B test results

        Args:
            test_name: Name of the test
            results: Test results data

        Returns:
            Test analysis and recommendation
        """
        logger.info(f"Analyzing A/B test: {test_name}...")

        results_text = ""
        if results:
            for variant, data in results.items():
                if isinstance(data, dict):
                    results_text += f"- {variant}: Conversion={data.get('conversion', 'N/A')}%, Sample={data.get('sample_size', 'N/A')}\n"
                else:
                    results_text += f"- {variant}: {data}\n"
        else:
            results_text = "No results data provided"

        prompt = f"""
ROLE: Experimentation Analyst
CONTEXT: Analyzing A/B test for {self.user_name}

TEST NAME: {test_name}

RESULTS:
{results_text}

TASK:
Analyze this A/B test:

## A/B Test Analysis: {test_name}

### Summary
| Variant | Primary Metric | Sample Size | Confidence |

### Statistical Analysis
- Sample Size: [Adequate / Insufficient]
- Duration: [Recommendation]
- Confidence Level: [X%]
- Statistical Significance: [Yes / No / Needs more data]

### Results Interpretation
What do these results tell us?

### Recommendation
**[Ship / Iterate / Kill / Continue Testing]**

Rationale: [Why this recommendation]

### Caveats
- [Important consideration]

### Next Steps
1. [Immediate action]
2. [Follow-up action]

### Learning
What did we learn from this test?

Be rigorous about statistical significance. Don't over-interpret.
"""

        system_prompt = """You are an experimentation expert. Be rigorous about
statistical analysis and honest about uncertainty."""

        try:
            analysis = self.generate_ai_response(
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=1200,
                temperature=0.4
            )
            logger.info("A/B test analysis complete")
            return analysis

        except Exception as e:
            logger.error(f"Error analyzing A/B test: {e}")
            raise

    def send_metrics_review_to_messaging(self, review: str) -> None:
        """Send metrics review to messaging"""
        self.send_to_messaging(review, title="Daily Metrics Review")

    def send_ab_analysis_to_messaging(self, analysis: str) -> None:
        """Send A/B test analysis to messaging"""
        self.send_to_messaging(analysis, title="A/B Test Results")


# Global instance
analytics_agent = AnalyticsAgent()


if __name__ == "__main__":
    print("Testing Analytics Agent...")
    print("=" * 50)

    try:
        review = analytics_agent.generate_metrics_review(
            metrics={
                "DAU": {"value": 12500, "target": 15000, "trend": "+5%"},
                "Activation Rate": {"value": "32%", "target": "40%", "trend": "+2%"},
                "Churn": {"value": "8%", "target": "5%", "trend": "-1%"},
            }
        )
        print("\nGenerated Metrics Review:")
        print("-" * 50)
        print(review)
        print("\n" + "=" * 50)
        print("✅ Analytics Agent test successful")

    except Exception as e:
        print(f"❌ Test failed: {e}")
