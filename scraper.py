import os
import random
import requests
from supabase import create_client
from duckduckgo_search import DDGS

# 1. Connect to your Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

def check_ssl(website_url):
    """Checks if a website is missing SSL (Security)"""
    if not website_url.startswith('http'):
        website_url = 'http://' + website_url
    try:
        # We try to connect. If it fails due to an SSL error, it's a lead!
        requests.get(website_url, timeout=5)
        return False
    except requests.exceptions.SSLError:
        return True
    except:
        return False

def start_hunting():
    # 2. Pick a random niche and city to keep the data fresh
    niches = ["Plumber", "Roofer", "Dentist", "HVAC", "Lawyer", "Landscaper"]
    cities = ["Austin", "Miami", "Chicago", "Denver", "Seattle", "Phoenix"]
    
    query = f"{random.choice(niches)} in {random.choice(cities)} official website"
    print(f"Hunting for: {query}")

    # 3. Use DuckDuckGo (Free) to find business websites
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=15)
        
        for r in results:
            site_url = r.get('href')
            business_name = r.get('title', 'Unknown Business').split('-')[0]
            
            if site_url and "facebook" not in site_url and "yelp" not in site_url:
                print(f"Checking: {site_url}")
                
                # 4. Check if the site is broken/insecure
                if check_ssl(site_url):
                    print(f"!!! FOUND SECURE ERROR: {business_name}")
                    
                    # 5. Save to Supabase
                    lead_data = {
                        "business_name": business_name,
                        "website": site_url,
                        "issue_found": "No SSL/Insecure Website"
                    }
                    supabase.table("leads").insert(lead_data).execute()

if __name__ == "__main__":
    start_hunting()
