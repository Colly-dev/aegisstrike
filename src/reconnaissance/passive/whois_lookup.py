"""
AegisStrike - WHOIS Lookup (Passive Reconnaissance)
Phase: Passive Reconnaissance
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import whois
from typing import Optional

def run(target: str) -> dict:
    """Perform WHOIS lookup on the target domain."""
    try:
        w = whois.whois(target)
        return {
            "registrar": str(w.registrar),
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "emails": w.emails,
            "org": str(w.org),
        }
    except Exception as e:
        return {"error": str(e)}
