"""
AegisStrike - Parameter Discovery
Phase: Web Enumeration
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import requests
from bs4 import BeautifulSoup
from typing import List

DEFAULT_PARAMS = ["id", "page", "search", "q", "query", "user", "username", "email", "token", "key", "file", "path", "url", "redirect", "next", "callback", "action", "type", "cat", "category"]

def run(target: str, timeout: int = 10) -> dict:
    """Discover URL parameters and form fields."""
    base_url = target if target.startswith("http") else f"http://{target}"
    params_found = []
    forms_found = []
    
    try:
        resp = requests.get(base_url, timeout=timeout)
        soup = BeautifulSoup(resp.text, 'lxml')
        
        # Extract form parameters
        for form in soup.find_all('form'):
            form_data = {"action": form.get('action', ''), "method": form.get('method', 'get'), "inputs": []}
            for inp in form.find_all(['input', 'select', 'textarea']):
                name = inp.get('name')
                if name:
                    form_data["inputs"].append(name)
            forms_found.append(form_data)
        
        # Extract URL parameters from links
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '?' in href:
                query = href.split('?', 1)[1]
                for param in query.split('&'):
                    key = param.split('=')[0]
                    if key and key not in params_found:
                        params_found.append(key)
    except Exception as e:
        return {"error": str(e), "params": [], "forms": []}
    
    return {"params": params_found, "forms": forms_found, "count": len(params_found)}
