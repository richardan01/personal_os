"""
Read data from Lark Base and format it for Discovery Agent analysis
This script fetches records from your Lark Base and prepares them for AI analysis
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.lark_client import lark_client
from utils.ai_client import ai_client
from config import settings
import json


def fetch_base_records(base_url: str):
    """
    Fetch all records from a Lark Base URL

    Args:
        base_url: Full Lark Base URL

    Returns:
        List of records or None
    """
    print("📊 Fetching data from Lark Base...")
    print("=" * 60)

    # Parse the URL
    parsed = lark_client.parse_base_url(base_url)
    if not parsed:
        print("❌ Failed to parse Base URL")
        print("Expected format: https://xxx.larksuite.com/base/APP_TOKEN?table=TABLE_ID&view=VIEW_ID")
        return None

    app_token = parsed['app_token']
    table_id = parsed['table_id']
    view_id = parsed['view_id']

    print(f"✅ Parsed URL successfully")
    print(f"   App Token: {app_token}")
    print(f"   Table ID: {table_id}")
    print(f"   View ID: {view_id}")
    print()

    # Fetch all records
    print("Fetching records...")
    records = lark_client.get_all_base_records(
        app_token=app_token,
        table_id=table_id,
        view_id=view_id,
        max_records=1000  # Adjust as needed
    )

    if records:
        print(f"✅ Retrieved {len(records)} record(s)")
        return records
    else:
        print("❌ Failed to fetch records")
        print("\nPossible issues:")
        print("1. Missing permissions - Add 'bitable:app' scope to your Lark app")
        print("2. Base access - Grant your bot read access to the base")
        print("3. Invalid credentials - Check LARK_APP_ID and LARK_APP_SECRET in .env")
        return None


def format_for_discovery_agent(records):
    """
    Format Lark Base records for Discovery Agent analysis

    Args:
        records: List of Lark Base records

    Returns:
        Formatted text suitable for Discovery Agent
    """
    print("\n📝 Formatting records for Discovery Agent...")
    print("=" * 60)

    formatted_text = "# User Feedback Data from Lark Base\n\n"

    for i, record in enumerate(records, 1):
        fields = record.get('fields', {})

        formatted_text += f"## Record {i}\n\n"

        for field_name, value in fields.items():
            # Handle different field types
            if isinstance(value, list):
                value = ", ".join(str(v) for v in value)
            elif isinstance(value, dict):
                value = json.dumps(value, ensure_ascii=False)

            formatted_text += f"**{field_name}**: {value}\n\n"

        formatted_text += "---\n\n"

    return formatted_text


def save_to_file(content: str, filename: str = "lark_base_data.txt"):
    """Save formatted content to a file"""
    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Saved formatted data to: {filepath}")
    return filepath


def analyze_with_discovery_agent(formatted_data: str):
    """
    Analyze the formatted data using AI (Discovery Agent style)

    Args:
        formatted_data: Formatted text data

    Returns:
        AI analysis result
    """
    print("\n🤖 Analyzing with AI (Discovery Agent)...")
    print("=" * 60)

    prompt = f"""ROLE: User Research Analyst
CONTEXT: Analyzing user feedback data from Lark Base to extract actionable insights

FEEDBACK DATA:
{formatted_data}

TASK:
Analyze this feedback and extract:
1. Key pain points with severity ratings
2. Common themes and patterns
3. Feature requests
4. User sentiment
5. Recommended actions

OUTPUT FORMAT:
## Feedback Analysis Summary

### Key Pain Points:
List pain points with severity (High/Medium/Low), frequency, and impact

### Common Themes:
Identify recurring patterns across the feedback

### Feature Requests:
Priority table with urgency assessment

### User Sentiment:
Overall sentiment analysis (Positive/Negative/Mixed)

### Notable Quotes:
Direct verbatim quotes that capture the essence

### Recommended Actions:
- Immediate (this week)
- Short-term (this month)
- Long-term (this quarter)

### Tags:
Categorize by segment, feature area, pain point
"""

    try:
        analysis = ai_client.generate(prompt, max_tokens=4000)
        print("✅ Analysis complete!")
        return analysis
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return None


def main():
    """Main execution function"""
    print("\n" + "=" * 60)
    print("  LARK BASE → DISCOVERY AGENT")
    print("  Read feedback from Lark and analyze with AI")
    print("=" * 60)

    # Your Lark Base URL
    base_url = "https://pj4w2l1pwuq.sg.larksuite.com/base/Adgxb8OxhaALzSstbuMlJsI2gQd?table=tblfeqt94MooBQ8W&view=vewhzzGdMk"

    # Step 1: Fetch records from Lark Base
    records = fetch_base_records(base_url)

    if not records:
        print("\n❌ Could not fetch records. Please check:")
        print("1. LARK_APP_ID and LARK_APP_SECRET are set in .env")
        print("2. Your Lark app has 'bitable:app' permission")
        print("3. Your bot has access to the base")
        print("\nSee LARK_SETUP.md for detailed instructions")
        return

    # Step 2: Format for Discovery Agent
    formatted_data = format_for_discovery_agent(records)

    # Step 3: Save to file
    filepath = save_to_file(formatted_data)

    # Step 4: Analyze with AI (if AI is configured)
    if settings.anthropic_api_key or settings.openai_api_key:
        print("\nWould you like to analyze this data with AI now? (y/n): ", end="")
        response = input().strip().lower()

        if response == 'y':
            analysis = analyze_with_discovery_agent(formatted_data)

            if analysis:
                # Save analysis
                analysis_file = save_to_file(analysis, "lark_base_analysis.txt")
                print(f"\n{'=' * 60}")
                print("📊 ANALYSIS RESULTS")
                print('=' * 60)
                print(analysis)
                print(f"\n{'=' * 60}")
                print(f"Analysis saved to: {analysis_file}")
    else:
        print("\n💡 Tip: Configure AI (ANTHROPIC_API_KEY or OPENAI_API_KEY)")
        print("   to automatically analyze this data with Discovery Agent")

    # Summary
    print("\n" + "=" * 60)
    print("  COMPLETE!")
    print("=" * 60)
    print(f"\n✅ Retrieved {len(records)} records from Lark Base")
    print(f"✅ Formatted data saved to: {filepath}")
    print("\nNext steps:")
    print("1. Review the formatted data")
    print("2. Copy it to Claude.ai or ChatGPT with Discovery Agent prompt")
    print("3. Get actionable insights from your feedback!")
    print()


if __name__ == "__main__":
    main()
