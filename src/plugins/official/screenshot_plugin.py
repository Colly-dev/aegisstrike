"""
AegisStrike - Screenshot Plugin
Captures website screenshots for visual documentation.
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

import shutil
import subprocess
import os
from plugins.plugin_base import PluginBase

class Plugin(PluginBase):
    name = "screenshot"
    description = "Website screenshot capture for visual documentation"
    version = "1.0.0"
    author = "AegisStrike"

    def is_available(self) -> bool:
        return shutil.which("chromium") is not None or shutil.which("google-chrome") is not None

    def run(self, target: str, output_dir: str = "reports/screenshots", **kwargs) -> dict:
        """Capture a screenshot of the target website."""
        if not self.is_available():
            return {"error": "chromium/chrome not installed", "available": False}
        
        os.makedirs(output_dir, exist_ok=True)
        base_url = target if target.startswith("http") else f"http://{target}"
        output_file = os.path.join(output_dir, f"{target.replace('/', '_')}.png")
        browser = shutil.which("chromium") or shutil.which("google-chrome")
        
        try:
            subprocess.run([
                browser, "--headless", "--no-sandbox", "--disable-gpu",
                f"--screenshot={output_file}", base_url
            ], capture_output=True, timeout=30)
            return {"available": True, "screenshot": output_file, "url": base_url}
        except Exception as e:
            return {"error": str(e), "available": True}
