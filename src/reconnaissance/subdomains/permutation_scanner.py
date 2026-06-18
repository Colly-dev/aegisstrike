"""
AegisStrike - Subdomain Permutation Scanner
Phase: Subdomain Enumeration
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import dns.resolver
from typing import List

PERMUTATION_PREFIXES = ["dev", "staging", "test", "api", "admin", "mail", "vpn", "cdn", "beta", "prod", "internal"]
PERMUTATION_SUFFIXES = ["-dev", "-staging", "-test", "-api", "-admin", "-prod", "-beta", "-old", "-new"]

def generate_permutations(base: str, domain: str) -> List[str]:
    """Generate subdomain permutations."""
    perms = []
    for prefix in PERMUTATION_PREFIXES:
        perms.append(f"{prefix}-{base}.{domain}")
        perms.append(f"{prefix}.{base}.{domain}")
    for suffix in PERMUTATION_SUFFIXES:
        perms.append(f"{base}{suffix}.{domain}")
    return perms

def run(target: str, known_subs: List[str] = None) -> dict:
    """Scan permutations of known subdomains."""
    if not known_subs:
        known_subs = ["www", "mail", "api"]
    found = []
    for sub in known_subs:
        base = sub.split(".")[0]
        perms = generate_permutations(base, target)
        for perm in perms:
            try:
                dns.resolver.resolve(perm, 'A')
                found.append(perm)
            except Exception:
                pass
    return {"found": found, "count": len(found)}
