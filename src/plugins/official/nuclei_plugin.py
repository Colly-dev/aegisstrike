"""
AegisStrike - Nuclei Plugin
Integrates Nuclei template-based scanning.
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import subprocess
import shutil
import json
from plugins.plugin_base import PluginBase

class Plugin(PluginBase):
    name = "nuclei"
    description = "Nuclei template-based vulnerability scanner integration"
    version = "1.0.0"
    author = "AegisStrike"

    def is_available(self) -> bool:
        return shutil.which("nuclei") is not None

    def run(self, target: str, **kwargs) -> dict:
        """Run nuclei against the target if available."""
        if not self.is_available():
            return {"error": "nuclei not installed", "available": False}
        
        base_url = target if target.startswith("http") else f"http://{target}"
        try:
            result = subprocess.run(
                ["nuclei", "-u", base_url, "-j", "-severity", "medium,high,critical", "-silent"],
                capture_output=True, text=True, timeout=300
            )
            findings = []
            for line in result.stdout.splitlines():
                try:
                    findings.append(json.loads(line))
                except Exception:
                    pass
            return {"available": True, "findings": findings, "count": len(findings)}
        except Exception as e:
            return {"error": str(e), "available": True}
