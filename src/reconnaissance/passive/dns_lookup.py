"""
AegisStrike - DNS Lookup (Passive Reconnaissance)
Phase: Passive Reconnaissance
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import dns.resolver
from typing import dict as Dict

def run(target: str) -> dict:
    """Perform DNS lookups for A, AAAA, MX, TXT, NS records."""
    results = {}
    record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME']
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(target, rtype)
            results[rtype] = [str(r) for r in answers]
        except Exception:
            results[rtype] = []
    return results
