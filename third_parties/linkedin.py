import os
import requests
import json
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()


PROFILES_DIR = "profiles"

def _profile_cache_handler(linkedin_profile: str, data: dict = None):
    """
        Loads or Saves profile data to local cache.
        - If data is None: Loads from cache (if exists).
        - If data is provided: Saves data to cache.
    """
    os.makedirs(PROFILES_DIR, exist_ok=True)
    profile_file = os.path.join(PROFILES_DIR, f"{linkedin_profile}.json")

    if data is None:
        # Load from cache
        if os.path.exists(profile_file):
            with open(profile_file, "r") as f:
                print(f"Loaded profile '{linkedin_profile}' from cache.")
                return json.load(f)
        return None
    else:
        # Save to cache
        with open(profile_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Fetched and cached profile '{linkedin_profile}'.")
        return data

def _get_profile_name_from_url(linkedin_profile_url: str) -> str:
    # Step 1: Extract URL if input is in Markdown link format
    if '(' in linkedin_profile_url and ')' in linkedin_profile_url:
        url = linkedin_profile_url.split('(')[1].split(')')[0]
    else:
        url = linkedin_profile_url  # Plain URL provided

    # Step 2: Extract LinkedIn profile name from URL
    if '/in/' in url:
        profile_name = url.split('/in/')[1].split('/')[0]
        return profile_name
    else:
        return ''  # Not a LinkedIn profile URL


def scrape_linkedin_profile(linkedin_profile: str, mock: bool = False):
    """
    Scrape information from LinkedIn profiles
    Manually scrape the information from LinkedIn profiles
    """
    print(f"Scraping profile '{_get_profile_name_from_url(linkedin_profile)}'")
    linkedin_profile = _get_profile_name_from_url(linkedin_profile)
    cached_profile = _profile_cache_handler(linkedin_profile)
    if cached_profile:
        return cached_profile

    api_key = os.getenv("SCRAPINGDOG_API_KEY")
    if not api_key:
        raise ValueError("SCRAPINGDOG_API_KEY environment variable is not set")

    # Otherwise, make API call
    url = "https://api.scrapingdog.com/linkedin"

    request_params = {
        "api_key": api_key,
        "type": "profile",
        "linkId": linkedin_profile,
        "premium": "false"
    }

    response = requests.get(url, params=request_params)

    if response.status_code == 200:
        data = response.json()
        # If API response is a list with a single dict, unwrap it.
        if isinstance(data, list) and len(data) == 1 and isinstance(data[0], dict):
            data = data[0]
        # Save the profile to file for caching
        _profile_cache_handler(linkedin_profile, data)
        return data
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None

if __name__ == "__main__":
    # print(scrape_linkedin_profile("anshulchoudhary90"))
    res = _get_profile_name_from_url("[https://in.linkedin.com/in/anshulchoudhary90](https://in.linkedin.com/in/anshulchoudhary90)")
    print(res)