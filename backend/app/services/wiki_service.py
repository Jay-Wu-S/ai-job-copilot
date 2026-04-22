from typing import List, Dict, Optional
from urllib.parse import quote

import requests


WIKI_API_BASE = "https://en.wikipedia.org/w/api.php"
WIKI_SUMMARY_BASE = "https://en.wikipedia.org/api/rest_v1/page/summary"
COMMON_HEADERS = {
    "User-Agent": "AIJobCopilot/0.1 (local learning project; contact: example@example.com)",
    "Api-User-Agent": "AIJobCopilot/0.1"
}


def search_wikipedia(query: str, limit: int = 5) -> List[Dict]:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "utf8": 1,
        "srlimit": limit,
        "origin": "*"
    }

    response = requests.get(
        WIKI_API_BASE,
        params=params,
        headers=COMMON_HEADERS,
        timeout=15
    )
    response.raise_for_status()

    data = response.json()
    items = data.get("query", {}).get("search", [])

    return [
        {
            "title": item.get("title", ""),
            "snippet": item.get("snippet", ""),
            "pageid": item.get("pageid")
        }
        for item in items
    ]


def get_page_summary(title: str) -> Optional[Dict]:
    safe_title = quote(title.replace(" ", "_"), safe="")
    url = f"{WIKI_SUMMARY_BASE}/{safe_title}"

    response = requests.get(
        url,
        headers=COMMON_HEADERS,
        timeout=15
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()
    data = response.json()

    extract = data.get("extract") or ""
    if not extract.strip():
        return None

    return {
        "title": data.get("title", title),
        "extract": extract,
        "description": data.get("description", ""),
        "content_urls": data.get("content_urls", {})
    }


def query_wikipedia(query: str, limit: int = 3) -> List[Dict]:
    search_results = search_wikipedia(query, limit=limit)

    results = []
    for item in search_results:
        title = item["title"]
        summary = get_page_summary(title)
        if summary:
            results.append({
                "title": summary["title"],
                "description": summary.get("description", ""),
                "extract": summary.get("extract", ""),
                "snippet": item.get("snippet", ""),
                "url": summary.get("content_urls", {}).get("desktop", {}).get("page", "")
            })

    return results