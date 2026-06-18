"""
AegisStrike - ASN Lookup via bgpview.io
Phase: Intelligence Gathering
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests

def run(ip: str) -> dict:
    """Look up ASN information for an IP address using bgpview.io."""
    try:
        resp = requests.get(f"https://api.bgpview.io/ip/{ip}", timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            prefixes = data.get("data", {}).get("prefixes", [])
            asns = []
            for prefix in prefixes:
                asn_info = prefix.get("asn", {})
                asns.append({
                    "asn": asn_info.get("asn"),
                    "name": asn_info.get("name"),
                    "description": asn_info.get("description"),
                    "country_code": asn_info.get("country_code"),
                    "prefix": prefix.get("prefix"),
                })
            return {"ip": ip, "asns": asns, "count": len(asns)}
    except Exception as e:
        return {"error": str(e), "ip": ip}
    return {"ip": ip, "asns": []}
