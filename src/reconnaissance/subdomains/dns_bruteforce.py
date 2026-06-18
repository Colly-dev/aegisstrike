"""
AegisStrike - DNS Bruteforce Subdomain Enumeration
Phase: Subdomain Enumeration
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import dns.resolver
import time
from typing import List

def resolve_subdomain(subdomain: str, domain: str) -> Optional[str]:
    """Try to resolve a subdomain."""
    fqdn = f"{subdomain}.{domain}"
    try:
        answers = dns.resolver.resolve(fqdn, 'A')
        ips = [str(r) for r in answers]
        return {"subdomain": fqdn, "ips": ips}
    except Exception:
        return None

def run(target: str, wordlist_path: str = "wordlists/subdomains/subdomains.txt", rate_limit: float = 0.05) -> dict:
    """Bruteforce subdomains using a wordlist."""
    found = []
    try:
        with open(wordlist_path, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        words = ["www", "mail", "ftp", "admin", "api", "dev", "staging", "test", "vpn", "remote"]
    
    for word in words:
        result = resolve_subdomain(word, target)
        if result:
            found.append(result)
        time.sleep(rate_limit)
    return {"found": found, "count": len(found)}
