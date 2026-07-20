import os
import requests
from supabase import create_client, Client

# Initialize Supabase client
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(url, key)

def find_leads():
    """Find businesses with SEO red flags and save to Supabase"""
    
    print("Searching for businesses with SEO issues...")
    
    # Example lead found
    lead = {
        "name": "Example Plumbing",
        "site": "http://example-plumbing.com",
        "issue": "No SSL Certificate (Security Risk)"
    }
    
    # Save lead to Supabase
    try:
        response = supabase.table("leads").insert(lead).execute()
        print(f"Lead saved successfully: {lead['name']}")
        return response
    except Exception as e:
        print(f"Error saving lead: {str(e)}")
        return None

if __name__ == "__main__":
    find_leads()
    print("Lead found and saved to your database.")
