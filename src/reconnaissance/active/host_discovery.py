"""
AegisStrike - Host Discovery (Active Reconnaissance)
Phase: Active Reconnaissance
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
WARNING: This module makes direct contact with the target.
"""

import subprocess
import socket
from typing import Optional

def run(target: str, timeout: int = 5) -> dict:
    """Check host availability via ICMP ping and TCP socket."""
    results = {"target": target, "alive": False, "methods": []}
    # TCP socket check
    for port in [80, 443, 22]:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            if result == 0:
                results["alive"] = True
                results["methods"].append(f"TCP:{port}")
                break
        except Exception:
            pass
    # ICMP ping
    try:
        ping = subprocess.run(["ping", "-c", "1", "-W", str(timeout), target], capture_output=True, timeout=timeout+2)
        if ping.returncode == 0:
            results["alive"] = True
            results["methods"].append("ICMP")
    except Exception:
        pass
    return results
