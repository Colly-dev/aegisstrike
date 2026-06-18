"""
AegisStrike - Notification Manager
Handles alerts, notifications, and output formatting.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from typing import List

console = Console()

class NotificationManager:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.alerts = []

    def alert(self, message: str, severity: str = "info"):
        """Generate an alert."""
        colors = {"critical": "bold red", "high": "red", "medium": "yellow", "low": "cyan", "info": "green"}
        color = colors.get(severity, "white")
        console.print(f"[{color}][{severity.upper()}] {message}[/{color}]")
        self.alerts.append({"message": message, "severity": severity})

    def finding(self, title: str, details: dict, severity: str = "info"):
        """Display a finding in a formatted panel."""
        colors = {"critical": "red", "high": "red", "medium": "yellow", "low": "cyan", "info": "green"}
        color = colors.get(severity, "white")
        content = "\n".join([f"{k}: {v}" for k, v in details.items()])
        console.print(Panel(content, title=f"[{color}][{severity.upper()}] {title}[/{color}]", border_style=color))

    def summary_table(self, title: str, rows: List[dict]):
        """Display a summary table."""
        if not rows:
            return
        table = Table(title=title)
        if rows:
            for key in rows[0].keys():
                table.add_column(key.capitalize(), style="cyan")
            for row in rows:
                table.add_row(*[str(v) for v in row.values()])
        console.print(table)

    def get_alerts(self) -> List[dict]:
        return self.alerts
