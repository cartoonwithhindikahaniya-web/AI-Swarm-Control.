import os
import requests
import json
from typing import List, Dict, Any

def web_search(query: str, num_results: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a web search using Serper API.
    """
    serper_api_key = os.getenv("SERPER_API_KEY")
    if not serper_api_key:
        return [{"error": "Serper API key not found."}]

    url = "https://google.serper.dev/search"
    payload = json.dumps({
        "q": query,
        "num": num_results
    })
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json()

        search_results = []
        if "organic" in results:
            for item in results["organic"]:
                search_results.append({
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "snippet": item.get("snippet")
                })
        return search_results
    except Exception as e:
        return [{"error": f"Search failed: {str(e)}"}]

def get_page_content(url: str) -> str:
    """
    Fetch the content of a web page.
    For simplicity, this just returns the raw text from the snippet if full scraping is not needed,
    but in a real scenario, this would use a scraper.
    """
    # This is a placeholder for a more robust scraping logic
    return f"Content of {url} would be fetched here."
