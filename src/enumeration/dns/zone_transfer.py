"""
AegisStrike - DNS Zone Transfer
Phase: DNS Enumeration
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import dns.resolver
import dns.zone
import dns.query
from typing import List

def run(target: str) -> dict:
    """Attempt DNS zone transfer (AXFR) against all nameservers."""
    results = {"target": target, "nameservers": [], "zone_transfer": False, "records": []}
    try:
        ns_records = dns.resolver.resolve(target, 'NS')
        for ns in ns_records:
            ns_host = str(ns).rstrip('.')
            results["nameservers"].append(ns_host)
            try:
                zone = dns.zone.from_xfr(dns.query.xfr(ns_host, target, timeout=10))
                results["zone_transfer"] = True
                for name, node in zone.nodes.items():
                    results["records"].append(str(name))
            except Exception:
                pass
    except Exception as e:
        results["error"] = str(e)
    return results
