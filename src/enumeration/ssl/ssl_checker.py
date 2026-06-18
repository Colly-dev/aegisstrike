"""
AegisStrike - SSL/TLS Certificate Checker
Phase: SSL/TLS Enumeration
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import ssl
import socket
from datetime import datetime

def run(target: str, port: int = 443) -> dict:
    """Check SSL/TLS certificate details and weak ciphers."""
    result = {"target": target, "port": port}
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((target, port), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                protocol = ssock.version()
                
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (not_after - datetime.utcnow()).days
                
                result.update({
                    "subject": dict(x[0] for x in cert.get('subject', [])),
                    "issuer": dict(x[0] for x in cert.get('issuer', [])),
                    "not_before": cert.get('notBefore'),
                    "not_after": cert.get('notAfter'),
                    "days_remaining": days_left,
                    "expired": days_left < 0,
                    "protocol": protocol,
                    "cipher": cipher[0] if cipher else None,
                    "san": [v for t, v in cert.get('subjectAltName', []) if t == 'DNS'],
                    "weak_protocol": protocol in ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1'],
                })
    except Exception as e:
        result["error"] = str(e)
    return result
