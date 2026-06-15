# search_tools.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")

def search_web(topic):

    url = "https://www.searchapi.io/api/v1/search"

    params = {
        "engine": "google",
        "q": topic
    }

    headers = {
        "Authorization": f"Bearer {SEARCH_API_KEY}"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers
    )

    data = response.json()

    results = []

    for item in data.get("organic_results", [])[:5]:

        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })

    return results