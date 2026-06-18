"""
AegisStrike - Validators
Target validation, domain/IP/CIDR validation, and input sanitization.
"""

import re
import ipaddress
from typing import Tuple

DOMAIN_REGEX = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")

def is_valid_domain(domain: str) -> bool:
    """Validate a domain name."""
    domain = domain.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
    return bool(DOMAIN_REGEX.match(domain))

def is_valid_ip(ip: str) -> bool:
    """Validate an IP address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_cidr(cidr: str) -> bool:
    """Validate a CIDR notation."""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return "/" in cidr
    except ValueError:
        return False

def validate_target(target: str) -> Tuple[bool, str]:
    """Validate a target string and return (is_valid, type)."""
    target = target.strip().lower().replace("http://", "").replace("https://", "").split("/")[0]
    if not target:
        return False, "empty"
    if is_valid_ip(target):
        return True, "ip"
    if is_valid_cidr(target):
        return True, "cidr"
    if is_valid_domain(target):
        return True, "domain"
    return False, "invalid"

def sanitize_input(value: str) -> str:
    """Sanitize user input to prevent injection."""
    return re.sub(r'[;&|`$]', '', value).strip()
