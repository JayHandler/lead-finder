import os
import random
import requests
from supabase import create_client
from duckduckgo_search import DDGS

# 1. Connect to your Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase = create_client(url, key)

def check_website_issues(website_url):
    """Checks if a website has various issues"""
    if not website_url.startswith('http'):
        website_url = 'http://' + website_url
    
    issues = []
    
    try:
        response = requests.get(website_url, timeout=5, allow_redirects=True)
        
        # Check for slow response time
        if response.elapsed.total_seconds() > 3:
            issues.append("Slow Website (Poor Performance)")
        
        # Check for missing security headers
        if 'X-Frame-Options' not in response.headers:
            issues.append("Missing Security Headers")
        
        # Check for outdated technology
        if response.status_code == 200:
            content = response.text.lower()
            if 'wordpress' in content and len(content) < 5000:
                issues.append("Outdated WordPress Install")
        
        # Check SSL certificate
        try:
            requests.get('https://' + website_url.replace('http://', '').replace('https://', ''), 
                        timeout=5, verify=True)
        except:
            issues.append("SSL Certificate Issues")
    
    except requests.exceptions.Timeout:
        issues.append("Website Timeout (Server Issues)")
    except requests.exceptions.ConnectionError:
        issues.append("Connection Error")
    except:
        pass
    
    return issues if issues else ["Poor SEO Indicators"]

def start_hunting():
    # 2. Pick a random niche and city to keep the data fresh
    niches = ["Plumber", "Roofer", "Dentist", "HVAC", "Lawyer", "Landscaper", "Electrician", "Photographer"]
    cities = ["Austin", "Miami", "Chicago", "Denver", "Seattle", "Phoenix", "Portland", "Atlanta"]
    
    query = f"{random.choice(niches)} in {random.choice(cities)}"
    print(f"Hunting for: {query}")

    # 3. Use DuckDuckGo (Free) to find business websites
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=20)
            
            leads_found = 0
            for r in results:
                site_url = r.get('href')
                business_name = r.get('title', 'Unknown Business').split('-')[0].strip()
                
                # Filter out social media and review sites
                if site_url and all(x not in site_url.lower() for x in ["facebook", "yelp", "google", "instagram", "twitter"]):
                    print(f"Checking: {site_url}")
                    
                    # Check for issues
                    issues = check_website_issues(site_url)
                    
                    if issues:
                        print(f"Found issues: {business_name} - {issues[0]}")
                        
                        # Save to Supabase
                        lead_data = {
                            "business_name": business_name,
                            "website": site_url,
                            "issue_found": issues[0]
                        }
                        try:
                            supabase.table("leads").insert(lead_data).execute()
                            print(f"✓ Lead saved: {business_name}")
                            leads_found += 1
                        except Exception as e:
                            print(f"Error saving lead: {str(e)}")
            
            print(f"\nTotal leads found and saved: {leads_found}")
    except Exception as e:
        print(f"Error during search: {str(e)}")

if __name__ == "__main__":
    start_hunting()
