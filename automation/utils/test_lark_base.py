"""
Test script for Lark Base (Bitable) integration
Reads data from a Lark Base table
"""

import sys
import os

# Add parent directory to path to import config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lark_client import lark_client
from config import settings
import json


def test_parse_url():
    """Test URL parsing"""
    print("\n1. Testing URL Parsing...")
    print("=" * 60)

    # Example URL - replace with your actual URL
    test_url = "https://pj4w2l1pwuq.sg.larksuite.com/base/Adgxb8OxhaALzSstbuMlJsI2gQd?table=tblfeqt94MooBQ8W&view=vewhzzGdMk"

    result = lark_client.parse_base_url(test_url)

    if result:
        print("✅ Successfully parsed Base URL")
        print(f"   App Token: {result['app_token']}")
        print(f"   Table ID: {result['table_id']}")
        print(f"   View ID: {result['view_id']}")
        return result
    else:
        print("❌ Failed to parse URL")
        return None


def test_list_tables(app_token: str):
    """Test listing tables in a base"""
    print("\n2. Testing List Tables...")
    print("=" * 60)

    tables = lark_client.list_base_tables(app_token)

    if tables:
        print(f"✅ Found {len(tables)} table(s) in base:")
        for table in tables:
            table_id = table.get('table_id', 'N/A')
            table_name = table.get('name', 'Unnamed')
            print(f"   - {table_name} (ID: {table_id})")
        return tables
    else:
        print("❌ Failed to list tables")
        print("   Check that:")
        print("   - Your Lark app has 'bitable:app' permission")
        print("   - The app is added to the base with read access")
        return None


def test_get_records(app_token: str, table_id: str, view_id: str = None):
    """Test getting records from a table"""
    print("\n3. Testing Get Records...")
    print("=" * 60)

    result = lark_client.get_base_records(
        app_token=app_token,
        table_id=table_id,
        page_size=10,  # Get first 10 records
        view_id=view_id
    )

    if result:
        records = result.get('items', [])
        has_more = result.get('has_more', False)

        print(f"✅ Retrieved {len(records)} record(s)")
        print(f"   Has more records: {has_more}")

        if records:
            print(f"\n   Sample record fields:")
            first_record = records[0]
            fields = first_record.get('fields', {})
            for field_name, value in list(fields.items())[:5]:  # Show first 5 fields
                print(f"   - {field_name}: {value}")

            if len(fields) > 5:
                print(f"   ... and {len(fields) - 5} more fields")

        return records
    else:
        print("❌ Failed to get records")
        return None


def test_get_all_records(app_token: str, table_id: str):
    """Test getting all records with pagination"""
    print("\n4. Testing Get All Records (with pagination)...")
    print("=" * 60)

    records = lark_client.get_all_base_records(
        app_token=app_token,
        table_id=table_id,
        max_records=100  # Limit to 100 for testing
    )

    if records:
        print(f"✅ Retrieved total of {len(records)} record(s)")
        return records
    else:
        print("❌ Failed to get all records")
        return None


def display_records_for_discovery_agent(records):
    """Format records for use with Discovery Agent"""
    print("\n5. Formatting Records for Discovery Agent...")
    print("=" * 60)

    if not records:
        print("No records to format")
        return

    print("Sample formatted output for Discovery Agent:\n")

    for i, record in enumerate(records[:3], 1):  # Show first 3 records
        fields = record.get('fields', {})
        print(f"Record {i}:")
        print(json.dumps(fields, indent=2, ensure_ascii=False))
        print()

    if len(records) > 3:
        print(f"... and {len(records) - 3} more records")


def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("  LARK BASE INTEGRATION TEST")
    print("=" * 60)

    # Check if Lark is configured
    if not settings.lark_app_id or not settings.lark_app_secret:
        print("\n❌ Lark credentials not configured!")
        print("Please set LARK_APP_ID and LARK_APP_SECRET in .env file")
        print("See LARK_SETUP.md for setup instructions")
        return

    # Test 1: Parse URL
    parsed = test_parse_url()
    if not parsed:
        return

    app_token = parsed['app_token']
    table_id = parsed['table_id']
    view_id = parsed['view_id']

    # Test 2: List tables
    tables = test_list_tables(app_token)

    # Test 3: Get records (first page)
    records = test_get_records(app_token, table_id, view_id)

    # Test 4: Get all records
    if records:
        all_records = test_get_all_records(app_token, table_id)

        # Test 5: Format for Discovery Agent
        if all_records:
            display_records_for_discovery_agent(all_records)

    # Summary
    print("\n" + "=" * 60)
    print("  TEST COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("1. If tests passed: You can now read data from your Lark Base!")
    print("2. Use the records with Discovery Agent to analyze feedback")
    print("3. See LARK_SETUP.md for more examples")
    print("\nTo use in your code:")
    print("  from utils.lark_client import lark_client")
    print("  records = lark_client.get_all_base_records(app_token, table_id)")
    print()


if __name__ == "__main__":
    main()
