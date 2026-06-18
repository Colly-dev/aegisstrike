"""
AegisStrike - Port Scanner (nmap with socket fallback)
Phase: Port Enumeration
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import subprocess
import socket
import shutil
from typing import List

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443, 8888, 9200, 27017]

def _socket_scan(host: str, ports: List[int], timeout: int = 3) -> List[dict]:
    """Fallback socket-based port scanner."""
    open_ports = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except Exception:
                    service = "unknown"
                open_ports.append({"port": port, "state": "open", "service": service})
        except Exception:
            pass
    return open_ports

def _nmap_scan(host: str) -> List[dict]:
    """Run nmap and parse XML output."""
    try:
        result = subprocess.run(
            ["nmap", "-sV", "-oX", "-", "--top-ports", "100", host],
            capture_output=True, text=True, timeout=120
        )
        from xml.etree import ElementTree as ET
        root = ET.fromstring(result.stdout)
        ports = []
        for host_elem in root.findall('host'):
            for port_elem in host_elem.findall('ports/port'):
                state = port_elem.find('state')
                service = port_elem.find('service')
                if state is not None and state.get('state') == 'open':
                    ports.append({
                        "port": int(port_elem.get('portid')),
                        "state": "open",
                        "service": service.get('name', 'unknown') if service is not None else 'unknown',
                        "version": service.get('version', '') if service is not None else ''
                    })
        return ports
    except Exception:
        return []

def run(target: str, timeout: int = 3) -> dict:
    """Scan ports using nmap if available, else socket fallback."""
    method = "nmap" if shutil.which("nmap") else "socket"
    if method == "nmap":
        ports = _nmap_scan(target)
    else:
        ports = _socket_scan(target, COMMON_PORTS, timeout)
    return {"method": method, "open_ports": ports, "count": len(ports)}
