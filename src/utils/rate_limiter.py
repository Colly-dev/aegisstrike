"""
AegisStrike - Rate Limiter
Controls request rate to ensure respectful and legal scanning.
"""

import time
import threading

class RateLimiter:
    def __init__(self, requests_per_second: float = 10.0):
        self.rps = requests_per_second
        self.min_interval = 1.0 / requests_per_second
        self.last_request = 0.0
        self._lock = threading.Lock()

    def wait(self):
        """Wait if necessary to respect the rate limit."""
        with self._lock:
            now = time.time()
            elapsed = now - self.last_request
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
            self.last_request = time.time()

    def set_rate(self, rps: float):
        """Update the rate limit."""
        self.rps = rps
        self.min_interval = 1.0 / rps
