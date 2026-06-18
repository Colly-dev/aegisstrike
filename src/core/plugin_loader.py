"""
AegisStrike - Plugin Loader
Loads plugins from the plugins/ directory dynamically.
"""

import importlib
import os
from typing import List

PLUGIN_DIR = os.path.join(os.path.dirname(__file__), '../../src/plugins/official')

class PluginLoader:
    def __init__(self):
        self.plugins = []

    def load_plugins(self) -> List:
        """Load all plugins from the plugins directory."""
        for fname in os.listdir(PLUGIN_DIR):
            if fname.endswith('.py') and fname != '__init__.py':
                module_name = fname[:-3]
                try:
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(PLUGIN_DIR, fname))
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if hasattr(mod, 'Plugin'):
                        self.plugins.append(mod.Plugin())
                except Exception:
                    pass
        return self.plugins
