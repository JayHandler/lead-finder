import os
import sys
from supabase import create_client

# 1. Connect to your Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")

print(f"URL present: {bool(url)}")
print(f"Key present: {bool(key)}")
print(f"URL: {url}")

# Try to connect
try:
    supabase = create_client(url, key)
    print("✓ Supabase client created successfully")
except Exception as e:
    print(f"✗ Error creating client: {e}")
    sys.exit(1)

# Hardcoded test leads
test_leads = [
    {"business_name": "Test 1", "website": "https://test1.com", "issue_found": "Test issue 1"},
    {"business_name": "Test 2", "website": "https://test2.com", "issue_found": "Test issue 2"},
]

# Try to insert
for lead in test_leads:
    try:
        print(f"Inserting: {lead['business_name']}")
        response = supabase.table("leads").insert(lead).execute()
        print(f"✓ Success: {response}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
