"""
AegisStrike - Target Manager
Parses and validates target strings (domain, IP, CIDR).
"""

import socket
import re
import ipaddress
from typing import Optional

class TargetManager:
    def __init__(self, target: str):
        self.raw_target = target
        self.host = None
        self.ip = None
        self.is_domain = False
        self.is_ip = False
        self.is_cidr = False
        self._parse()

    def _parse(self):
        """Parse the target string into components."""
        target = self.raw_target.strip().lower()
        target = target.replace("http://", "").replace("https://", "").split("/")[0]
        self.host = target
        try:
            ipaddress.ip_network(target, strict=False)
            if "/" in target:
                self.is_cidr = True
            else:
                self.is_ip = True
                self.ip = target
        except ValueError:
            self.is_domain = True
            try:
                self.ip = socket.gethostbyname(target)
            except socket.gaierror:
                self.ip = None

    def is_valid(self) -> bool:
        """Validate the target format."""
        if not self.host:
            return False
        if self.is_ip or self.is_cidr:
            return True
        domain_regex = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$")
        return bool(domain_regex.match(self.host))

    def get_info(self) -> dict:
        return {"host": self.host, "ip": self.ip, "is_domain": self.is_domain, "is_ip": self.is_ip, "is_cidr": self.is_cidr}
