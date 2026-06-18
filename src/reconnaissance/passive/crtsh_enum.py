"""
AegisStrike - crt.sh Certificate Transparency Enumeration (Passive)
Phase: Passive Reconnaissance
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests
from typing import List

def run(target: str) -> dict:
    """Enumerate subdomains via crt.sh certificate transparency logs."""
    subdomains = set()
    try:
        url = f"https://crt.sh/?q=%.{target}&output=json"
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            for entry in data:
                name = entry.get("name_value", "")
                for sub in name.split("\n"):
                    sub = sub.strip().lower()
                    if sub.endswith(target):
                        subdomains.add(sub)
    except Exception as e:
        return {"error": str(e), "subdomains": []}
    return {"subdomains": sorted(list(subdomains)), "count": len(subdomains)}
