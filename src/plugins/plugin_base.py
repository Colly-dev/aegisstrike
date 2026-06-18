"""
AegisStrike - Plugin Base Class
Defines the interface for all AegisStrike plugins.
"""

from abc import ABC, abstractmethod

class PluginBase(ABC):
    name: str = "base"
    description: str = "Base plugin"
    version: str = "1.0.0"
    author: str = "AegisStrike"

    @abstractmethod
    def run(self, target: str, **kwargs) -> dict:
        """Execute the plugin against the target."""
        pass

    def is_available(self) -> bool:
        """Check if the plugin's dependencies are available."""
        return True

    def get_info(self) -> dict:
        return {"name": self.name, "description": self.description, "version": self.version, "author": self.author}
