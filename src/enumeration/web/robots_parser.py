"""
AegisStrike - Robots.txt Parser
Phase: Web Enumeration
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests
from typing import List

def run(target: str, timeout: int = 10) -> dict:
    """Parse robots.txt and detect sitemaps."""
    base_url = target if target.startswith("http") else f"http://{target}"
    disallowed = []
    allowed = []
    sitemaps = []
    
    try:
        resp = requests.get(f"{base_url}/robots.txt", timeout=timeout)
        if resp.status_code == 200:
            for line in resp.text.splitlines():
                line = line.strip()
                if line.lower().startswith("disallow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        disallowed.append(path)
                elif line.lower().startswith("allow:"):
                    path = line.split(":", 1)[1].strip()
                    if path:
                        allowed.append(path)
                elif line.lower().startswith("sitemap:"):
                    sitemap_url = line.split(":", 1)[1].strip()
                    sitemaps.append(sitemap_url)
    except Exception as e:
        return {"error": str(e), "disallowed": [], "allowed": [], "sitemaps": []}
    
    return {"disallowed": disallowed, "allowed": allowed, "sitemaps": sitemaps}
