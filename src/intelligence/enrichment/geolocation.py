"""
AegisStrike - IP Geolocation
Phase: Intelligence Gathering
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests

def run(ip: str) -> dict:
    """Geolocate an IP address using ip-api.com (free, no key required)."""
    try:
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                return {
                    "ip": ip,
                    "country": data.get("country"),
                    "region": data.get("regionName"),
                    "city": data.get("city"),
                    "isp": data.get("isp"),
                    "org": data.get("org"),
                    "lat": data.get("lat"),
                    "lon": data.get("lon"),
                    "timezone": data.get("timezone"),
                }
    except Exception as e:
        return {"error": str(e)}
    return {"ip": ip, "error": "geolocation failed"}
