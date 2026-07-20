import os
import random
import requests
from supabase import create_client
from duckduckgo_search import DDGS

# 1. Connect to your Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

def start_hunting():
    print("Starting lead hunt...")
    
    # TEST: First, let's try to save a test lead to verify Supabase connection works
    test_lead = {
        "business_name": "Test Business - Script Running",
        "website": "https://test.example.com",
        "issue_found": "Test Entry - Script Executed Successfully"
    }
    
    try:
        response = supabase.table("leads").insert(test_lead).execute()
        print(f"✓ Test lead saved successfully: {test_lead['business_name']}")
    except Exception as e:
        print(f"Error saving test lead: {str(e)}")
        return
    
    # 2. Pick a random niche and city
    niches = ["Plumber", "Roofer", "Dentist", "HVAC", "Lawyer", "Landscaper"]
    cities = ["Austin", "Miami", "Chicago", "Denver", "Seattle", "Phoenix"]
    
    query = f"{random.choice(niches)} in {random.choice(cities)}"
    print(f"Hunting for: {query}")

    # 3. Use DuckDuckGo to find business websites
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=10)
            print(f"Found {len(results)} search results")
            
            for r in results:
                site_url = r.get('href')
                business_name = r.get('title', 'Unknown Business').split('-')[0].strip()
                
                if site_url and all(x not in site_url.lower() for x in ["facebook", "yelp", "google", "instagram"]):
                    print(f"Found: {business_name} - {site_url}")
                    
                    # Save all found businesses as leads
                    lead_data = {
                        "business_name": business_name,
                        "website": site_url,
                        "issue_found": "Website Found - Review Required"
                    }
                    try:
                        supabase.table("leads").insert(lead_data).execute()
                        print(f"✓ Saved: {business_name}")
                    except Exception as e:
                        print(f"Error saving: {str(e)}")
    except Exception as e:
        print(f"Error during search: {str(e)}")

if __name__ == "__main__":
    start_hunting()
    print("Lead hunt completed!")
