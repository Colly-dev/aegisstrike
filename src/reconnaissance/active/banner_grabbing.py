"""
AegisStrike - Banner Grabbing (Active Reconnaissance)
Phase: Active Reconnaissance
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
WARNING: This module makes direct contact with the target.
"""

import socket
from typing import List

COMMON_PORTS = [21, 22, 23, 25, 80, 110, 143, 443, 3306, 5432, 8080, 8443]

def grab_banner(host: str, port: int, timeout: int = 5) -> Optional[str]:
    """Grab service banner from a specific port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
        sock.close()
        return banner[:200]
    except Exception:
        return None

def run(target: str, ports: List[int] = None) -> dict:
    """Grab banners from common service ports."""
    if ports is None:
        ports = COMMON_PORTS
    results = {}
    for port in ports:
        banner = grab_banner(target, port)
        if banner:
            results[str(port)] = banner
    return {"banners": results, "count": len(results)}
