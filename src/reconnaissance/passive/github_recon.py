"""
AegisStrike - GitHub Reconnaissance (Passive)
Phase: Passive Reconnaissance
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import os
import requests
from typing import List

GITHUB_API = "https://api.github.com/search/code"

def run(target: str) -> dict:
    """Search GitHub for references to the target domain."""
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    results = []
    try:
        resp = requests.get(GITHUB_API, headers=headers, params={"q": target, "per_page": 10}, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("items", []):
                results.append({"repo": item["repository"]["full_name"], "file": item["path"], "url": item["html_url"]})
        elif resp.status_code == 401:
            return {"error": "GitHub token required for code search", "results": []}
    except Exception as e:
        return {"error": str(e), "results": []}
    return {"results": results, "count": len(results)}
