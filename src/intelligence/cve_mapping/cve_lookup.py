"""
AegisStrike - CVE Lookup via NVD API
Phase: Intelligence Gathering
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests
import os

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"

FALLBACK_CVES = {
    "apache": [{"id": "CVE-2021-41773", "description": "Path traversal in Apache 2.4.49", "cvss": 7.5}],
    "nginx": [{"id": "CVE-2021-23017", "description": "Buffer overflow in nginx resolver", "cvss": 7.7}],
    "wordpress": [{"id": "CVE-2022-21661", "description": "SQL injection in WordPress", "cvss": 7.5}],
    "openssh": [{"id": "CVE-2023-38408", "description": "Remote code execution via ssh-agent", "cvss": 9.8}],
    "openssl": [{"id": "CVE-2022-0778", "description": "Infinite loop in BN_mod_sqrt()", "cvss": 7.5}],
    "php": [{"id": "CVE-2022-31625", "description": "Use after free in Postgres extension", "cvss": 8.1}],
}

def run(service_keyword: str) -> dict:
    """Query NVD API for CVEs related to a service keyword."""
    api_key = os.getenv("NVD_API_KEY")
    headers = {}
    if api_key:
        headers["apiKey"] = api_key
    
    try:
        params = {"keywordSearch": service_keyword, "resultsPerPage": 5}
        resp = requests.get(NVD_API, headers=headers, params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            cves = []
            for item in data.get("vulnerabilities", []):
                cve = item.get("cve", {})
                cve_id = cve.get("id", "")
                desc = cve.get("descriptions", [{}])[0].get("value", "")
                metrics = cve.get("metrics", {})
                cvss = 0.0
                if "cvssMetricV31" in metrics:
                    cvss = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
                elif "cvssMetricV2" in metrics:
                    cvss = metrics["cvssMetricV2"][0]["cvssData"]["baseScore"]
                cves.append({"id": cve_id, "description": desc[:200], "cvss": cvss})
            return {"service": service_keyword, "cves": cves, "source": "nvd"}
    except Exception:
        pass
    
    # Fallback dataset
    keyword_lower = service_keyword.lower()
    for key, cves in FALLBACK_CVES.items():
        if key in keyword_lower:
            return {"service": service_keyword, "cves": cves, "source": "fallback"}
    
    return {"service": service_keyword, "cves": [], "source": "fallback"}
