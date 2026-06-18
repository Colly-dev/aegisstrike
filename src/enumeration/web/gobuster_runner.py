"""
AegisStrike - Web Directory Enumeration (gobuster with requests fallback)
Phase: Web Enumeration
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import subprocess
import shutil
import requests
import time
from typing import List

DEFAULT_WORDLIST = "wordlists/directories/common.txt"

def _requests_scan(base_url: str, wordlist: str, timeout: int = 10) -> List[dict]:
    """Fallback requests-based directory brute forcer."""
    found = []
    try:
        with open(wordlist, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        words = ["admin", "login", "api", "backup", "config", "test", "dev", "uploads", "images", "js", "css"]
    
    for word in words:
        url = f"{base_url}/{word}"
        try:
            resp = requests.get(url, timeout=timeout, allow_redirects=False)
            if resp.status_code in [200, 301, 302, 403]:
                found.append({"url": url, "status": resp.status_code, "size": len(resp.content)})
            time.sleep(0.05)
        except Exception:
            pass
    return found

def run(target: str, wordlist: str = DEFAULT_WORDLIST, timeout: int = 10) -> dict:
    """Run directory enumeration using gobuster or requests fallback."""
    base_url = target if target.startswith("http") else f"http://{target}"
    method = "gobuster" if shutil.which("gobuster") else "requests"
    
    if method == "gobuster":
        try:
            result = subprocess.run(
                ["gobuster", "dir", "-u", base_url, "-w", wordlist, "-q", "--no-error"],
                capture_output=True, text=True, timeout=120
            )
            found = []
            for line in result.stdout.splitlines():
                if line.strip():
                    found.append({"raw": line.strip()})
            return {"method": "gobuster", "found": found, "count": len(found)}
        except Exception:
            pass
    
    found = _requests_scan(base_url, wordlist, timeout)
    return {"method": "requests", "found": found, "count": len(found)}
