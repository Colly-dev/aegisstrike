"""
AegisStrike - CMS Detector
Phase: Fingerprinting
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests
from typing import Optional

CMS_SIGNATURES = {
    "WordPress": ["/wp-login.php", "/wp-admin/", "wp-content", "wp-includes"],
    "Joomla": ["/administrator/", "Joomla!", "/components/com_"],
    "Drupal": ["Drupal.settings", "/sites/default/", "X-Generator: Drupal"],
    "Magento": ["/skin/frontend/", "Mage.Cookies", "/js/mage/"],
    "Shopify": ["cdn.shopify.com", "Shopify.theme"],
    "Wix": ["wix.com", "X-Wix-Published-Version"],
    "Squarespace": ["squarespace.com", "Squarespace"],
    "Django": ["csrfmiddlewaretoken", "django"],
    "Laravel": ["laravel_session", "X-Powered-By: PHP"],
}

def run(target: str, timeout: int = 10) -> dict:
    """Detect CMS via signature matching against response bodies and headers."""
    base_url = target if target.startswith("http") else f"http://{target}"
    detected = []
    
    try:
        resp = requests.get(base_url, timeout=timeout)
        body = resp.text.lower()
        headers = str(resp.headers).lower()
        
        for cms, signatures in CMS_SIGNATURES.items():
            for sig in signatures:
                if sig.lower() in body or sig.lower() in headers:
                    detected.append({"cms": cms, "signature": sig})
                    break
        
        # Check common CMS paths
        for cms, signatures in CMS_SIGNATURES.items():
            for sig in signatures:
                if sig.startswith("/"):
                    try:
                        r = requests.get(f"{base_url}{sig}", timeout=5, allow_redirects=False)
                        if r.status_code in [200, 301, 302, 403]:
                            if not any(d["cms"] == cms for d in detected):
                                detected.append({"cms": cms, "signature": sig, "path_found": True})
                    except Exception:
                        pass
    except Exception as e:
        return {"error": str(e), "detected": []}
    
    return {"detected": detected, "count": len(detected)}
