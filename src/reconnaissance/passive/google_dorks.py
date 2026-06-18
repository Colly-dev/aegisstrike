"""
AegisStrike - Google Dork Generator (Passive Reconnaissance)
Phase: Passive Reconnaissance
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
NOTE: This module GENERATES dork query strings ONLY. No automated Google searches are performed.
"""

def run(target: str) -> dict:
    """Generate Google dork queries for manual use."""
    dorks = [
        f"site:{target}",
        f"site:{target} filetype:pdf",
        f"site:{target} filetype:xls OR filetype:xlsx",
        f"site:{target} inurl:admin",
        f"site:{target} inurl:login",
        f"site:{target} intitle:\"index of\"",
        f"site:{target} inurl:config",
        f"site:{target} inurl:backup",
        f"site:{target} inurl:wp-admin",
        f"site:{target} inurl:phpinfo",
        f"site:{target} ext:sql",
        f"site:{target} ext:log",
        f"\"@{target}\" email",
        f"site:{target} intext:password",
        f"cache:{target}",
    ]
    instructions = "Copy and paste these queries into Google manually. Do NOT automate Google searches."
    return {"dorks": dorks, "count": len(dorks), "instructions": instructions}
