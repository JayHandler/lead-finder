import os
from supabase import create_client

# 1. Connect to your Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")

print(f"SUPABASE_URL: {url}")
print(f"SUPABASE_SERVICE_KEY: {'*' * 10}...")

supabase = create_client(url, key)

# Hardcoded test leads to verify Supabase connection works
test_leads = [
    {
        "business_name": "John's Plumbing Services",
        "website": "https://johnsplumbing.com",
        "issue_found": "Website needs SSL certificate update"
    },
    {
        "business_name": "Smith Roofing Company",
        "website": "https://smithroofing.net",
        "issue_found": "Contact form not working"
    },
    {
        "business_name": "Downtown HVAC Specialists",
        "website": "https://downtownhvac.com",
        "issue_found": "Missing business hours information"
    },
    {
        "business_name": "Green Landscaping LLC",
        "website": "https://greenlandscaping.io",
        "issue_found": "Portfolio images not loading"
    },
    {
        "business_name": "Elite Dental Studio",
        "website": "https://elitedentalstudio.com",
        "issue_found": "Patient reviews section outdated"
    }
]

print(f"\nAttempting to insert {len(test_leads)} test leads...")

for lead in test_leads:
    try:
        response = supabase.table("leads").insert(lead).execute()
        print(f"✓ Inserted: {lead['business_name']}")
    except Exception as e:
        print(f"✗ Error inserting {lead['business_name']}: {str(e)}")

print("\nScript completed!")
