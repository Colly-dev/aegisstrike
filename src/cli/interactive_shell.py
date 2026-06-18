"""
AegisStrike - Interactive Shell
Provides an interactive command shell with history and tab completion.
"""

import readline
import sys
from rich.console import Console

console = Console()

COMMANDS = {
    "scan": "Run a scan: scan <target> [--mode MODE]",
    "history": "Show scan history",
    "help": "Show this help message",
    "exit": "Exit the interactive shell",
    "clear": "Clear the screen",
}

def show_help():
    console.print("\n[bold cyan]AegisStrike Interactive Shell Commands:[/bold cyan]")
    for cmd, desc in COMMANDS.items():
        console.print(f"  [green]{cmd:<12}[/green] {desc}")
    console.print()

def run_interactive():
    """Start the interactive shell."""
    console.print("[bold red]AegisStrike[/bold red] [white]Interactive Shell[/white]")
    console.print("Type [green]help[/green] for available commands or [red]exit[/red] to quit.\n")
    
    history = []
    readline.set_history_length(100)
    
    while True:
        try:
            cmd = input("[aegisstrike]> ").strip()
            if not cmd:
                continue
            history.append(cmd)
            
            if cmd == "exit":
                console.print("[yellow]Goodbye![/yellow]")
                break
            elif cmd == "help":
                show_help()
            elif cmd == "history":
                for i, h in enumerate(history, 1):
                    console.print(f"  {i}: {h}")
            elif cmd == "clear":
                import os
                os.system('clear')
            elif cmd.startswith("scan "):
                parts = cmd.split()
                if len(parts) >= 2:
                    target = parts[1]
                    console.print(f"[cyan]Starting scan against {target}...[/cyan]")
                    console.print("[yellow]Use aegisstrike.py for full scan functionality.[/yellow]")
            else:
                console.print(f"[red]Unknown command: {cmd}[/red]. Type [green]help[/green] for available commands.")
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit.[/yellow]")
        except EOFError:
            break
