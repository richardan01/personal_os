"""
Simple test to read data from Lark Base
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from utils.lark_client import lark_client
import json

def main():
    """Test reading from Lark Base"""
    print("\n" + "=" * 60)
    print("  LARK BASE DATA READER")
    print("=" * 60)

    # Your Lark Base URL
    base_url = "https://pj4w2l1pwuq.sg.larksuite.com/base/Adgxb8OxhaALzSstbuMlJsI2gQd?table=tblfeqt94MooBQ8W&view=vewhzzGdMk"

    print("\n1. Parsing Base URL...")
    print("-" * 60)

    # Parse the URL
    parsed = lark_client.parse_base_url(base_url)

    if not parsed:
        print("❌ Failed to parse URL")
        return

    print(f"✅ Successfully parsed URL:")
    print(f"   App Token: {parsed['app_token']}")
    print(f"   Table ID: {parsed['table_id']}")
    print(f"   View ID: {parsed['view_id']}")

    app_token = parsed['app_token']
    table_id = parsed['table_id']
    view_id = parsed['view_id']

    print("\n2. Fetching records from Lark Base...")
    print("-" * 60)

    # Try to fetch records
    result = lark_client.get_base_records(
        app_token=app_token,
        table_id=table_id,
        page_size=10,  # Get first 10 records
        view_id=view_id
    )

    if not result:
        print("\n❌ Failed to fetch records")
        print("\nNext steps to fix:")
        print("1. Set up Lark credentials in .env file:")
        print("   LARK_APP_ID=cli_your_app_id_here")
        print("   LARK_APP_SECRET=your_app_secret_here")
        print()
        print("2. Add 'bitable:app' permission to your Lark app")
        print()
        print("3. Grant your bot access to the base:")
        print("   - Open the base in Lark")
        print("   - Click Share → Advanced Settings")
        print("   - Add your bot with Read permission")
        print()
        print("See LARK_BASE_INTEGRATION.md for detailed instructions")
        return

    records = result.get('items', [])
    has_more = result.get('has_more', False)

    print(f"✅ Retrieved {len(records)} record(s)")
    print(f"   Has more pages: {has_more}")

    if records:
        print("\n3. Sample Record Data:")
        print("-" * 60)

        # Show first record
        first_record = records[0]
        fields = first_record.get('fields', {})

        print(f"\nFirst record has {len(fields)} fields:")
        for field_name, value in fields.items():
            # Truncate long values
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:100] + "..."
            print(f"  {field_name}: {value_str}")

        # Save all records to file
        print("\n4. Saving data to file...")
        print("-" * 60)

        output_file = os.path.join(os.path.dirname(__file__), "lark_base_data.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(records)} records to: {output_file}")

        # Format for Discovery Agent
        text_file = os.path.join(os.path.dirname(__file__), "lark_base_data.txt")
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write("# User Feedback Data from Lark Base\n\n")

            for i, record in enumerate(records, 1):
                fields = record.get('fields', {})
                f.write(f"## Record {i}\n\n")

                for field_name, value in fields.items():
                    f.write(f"**{field_name}**: {value}\n\n")

                f.write("---\n\n")

        print(f"✅ Formatted text saved to: {text_file}")

    print("\n" + "=" * 60)
    print("  SUCCESS!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the data in lark_base_data.json or lark_base_data.txt")
    print("2. Copy the text file content to use with Discovery Agent")
    print("3. Analyze the feedback with AI!")
    print()

if __name__ == "__main__":
    main()
