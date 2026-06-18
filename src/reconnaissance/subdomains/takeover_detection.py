"""
AegisStrike - Subdomain Takeover Detection
Phase: Subdomain Enumeration
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests
from typing import List

TAKEOVER_FINGERPRINTS = {
    "github": ["There isn't a GitHub Pages site here", "github.com"],
    "heroku": ["No such app", "herokuapp.com"],
    "s3": ["NoSuchBucket", "s3.amazonaws.com"],
    "fastly": ["Fastly error: unknown domain", "fastly.com"],
    "shopify": ["Sorry, this shop is currently unavailable", "myshopify.com"],
    "zendesk": ["Help Center Closed", "zendesk.com"],
    "bitbucket": ["Repository not found", "bitbucket.io"],
    "ghost": ["The thing you were looking for is no longer here", "ghost.io"],
    "cargo": ["If you're moving your domain away from Cargo", "cargocollective.com"],
    "tumblr": ["Whatever you were looking for doesn't currently exist", "tumblr.com"],
}

def check_takeover(subdomain: str) -> dict:
    """Check if a subdomain is vulnerable to takeover."""
    for provider, (fingerprint, cname_hint) in TAKEOVER_FINGERPRINTS.items():
        try:
            resp = requests.get(f"http://{subdomain}", timeout=10, allow_redirects=True)
            if fingerprint.lower() in resp.text.lower():
                return {"subdomain": subdomain, "vulnerable": True, "provider": provider, "fingerprint": fingerprint}
        except Exception:
            pass
    return {"subdomain": subdomain, "vulnerable": False}

def run(subdomains: List[str]) -> dict:
    """Check a list of subdomains for takeover vulnerabilities."""
    vulnerable = []
    for sub in subdomains:
        result = check_takeover(sub)
        if result.get("vulnerable"):
            vulnerable.append(result)
    return {"vulnerable": vulnerable, "count": len(vulnerable)}
