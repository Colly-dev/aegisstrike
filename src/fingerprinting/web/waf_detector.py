"""
AegisStrike - WAF Detector
Phase: Fingerprinting
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests

WAF_SIGNATURES = {
    "Cloudflare": ["CF-RAY", "cloudflare", "__cfduid", "cf-cache-status"],
    "AWS WAF": ["x-amzn-requestid", "x-amz-cf-id", "awselb"],
    "Akamai": ["akamai", "x-akamai-transformed", "x-check-cacheable"],
    "Sucuri": ["x-sucuri-id", "sucuri", "x-sucuri-cache"],
    "Imperva": ["x-iinfo", "incapsula", "visid_incap"],
    "F5 BIG-IP": ["x-wa-info", "bigipserver", "f5"],
    "Barracuda": ["barra_counter_session", "barracuda"],
    "ModSecurity": ["mod_security", "modsecurity"],
    "Nginx WAF": ["naxsi", "nginx"],
}

def run(target: str, timeout: int = 10) -> dict:
    """Detect WAF via headers and response signature matching."""
    base_url = target if target.startswith("http") else f"http://{target}"
    detected = []
    
    try:
        resp = requests.get(base_url, timeout=timeout)
        headers_str = str(resp.headers).lower()
        body = resp.text.lower()
        
        for waf, signatures in WAF_SIGNATURES.items():
            for sig in signatures:
                if sig.lower() in headers_str or sig.lower() in body:
                    detected.append({"waf": waf, "signature": sig})
                    break
    except Exception as e:
        return {"error": str(e), "detected": []}
    
    return {"detected": detected, "count": len(detected)}
