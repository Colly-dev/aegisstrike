"""
AegisStrike - Configuration Loader
Loads and validates configuration from config/config.yaml.
"""

import os
import yaml
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG = {
    "scanning": {"threads": 10, "timeout": 30, "rate_limit": 10, "user_agent": "AegisStrike/1.0"},
    "modules": {"passive": True, "active": True, "subdomains": True, "ports": True, "web": True, "fingerprinting": True, "vulns": True},
}

def load_config(config_path: str = None) -> dict:
    """Load configuration from YAML file with environment variable overrides."""
    config = DEFAULT_CONFIG.copy()
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            file_config = yaml.safe_load(f)
            if file_config:
                config.update(file_config)
    # Environment overrides
    if os.getenv("AEGIS_THREADS"):
        config["scanning"]["threads"] = int(os.getenv("AEGIS_THREADS"))
    if os.getenv("AEGIS_TIMEOUT"):
        config["scanning"]["timeout"] = int(os.getenv("AEGIS_TIMEOUT"))
    return config
