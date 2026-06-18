"""
AegisStrike - Cloud/CDN Provider Detection
Phase: Fingerprinting
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests
import socket

CLOUD_SIGNATURES = {
    "AWS": ["amazonaws.com", "aws", "cloudfront.net", "x-amz"],
    "Google Cloud": ["googleapis.com", "google", "gstatic.com", "x-goog"],
    "Azure": ["azure.com", "azureedge.net", "windows.net", "x-ms"],
    "Cloudflare": ["cloudflare.com", "cf-ray", "cloudflare"],
    "Fastly": ["fastly.com", "x-fastly", "fastly"],
    "Akamai": ["akamai.com", "akamaized.net", "akamai"],
    "DigitalOcean": ["digitalocean.com", "digitaloceanspaces.com"],
    "Heroku": ["heroku.com", "herokuapp.com"],
    "Vercel": ["vercel.app", "now.sh", "x-vercel"],
    "Netlify": ["netlify.com", "netlify.app", "x-nf-request-id"],
}

def run(target: str, timeout: int = 10) -> dict:
    """Detect cloud provider and CDN from headers and CNAME records."""
    base_url = target if target.startswith("http") else f"http://{target}"
    detected = []
    
    try:
        resp = requests.get(base_url, timeout=timeout)
        headers_str = str(resp.headers).lower()
        
        for provider, signatures in CLOUD_SIGNATURES.items():
            for sig in signatures:
                if sig.lower() in headers_str:
                    detected.append({"provider": provider, "signature": sig})
                    break
    except Exception as e:
        return {"error": str(e), "detected": []}
    
    # Check CNAME
    try:
        import dns.resolver
        cname = dns.resolver.resolve(target.replace("http://", "").replace("https://", "").split("/")[0], 'CNAME')
        for r in cname:
            cname_str = str(r).lower()
            for provider, sigs in CLOUD_SIGNATURES.items():
                for sig in sigs:
                    if sig.lower() in cname_str:
                        if not any(d["provider"] == provider for d in detected):
                            detected.append({"provider": provider, "cname": cname_str})
    except Exception:
        pass
    
    return {"detected": detected, "count": len(detected)}
