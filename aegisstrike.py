#!/usr/bin/env python3
"""
AegisStrike - Elite Reconnaissance & Automated Pentesting Framework

╔═══════════════════════════════════════════════════════════════════╗
║  ⚠️  LEGAL NOTICE - READ CAREFULLY  ⚠️                          ║
║                                                                  ║
║  AegisStrike is for EDUCATIONAL and AUTHORIZED testing only.    ║
║  Only scan systems you own or have permission to test.          ║
║                                                                  ║
║  By using this tool you agree to:                               ║
║    • Only scan authorized targets                               ║
║    • Comply with all laws                                       ║
║    • Accept full responsibility                                 ║
║                                                                  ║
║  The authors assume NO LIABILITY for misuse.                    ║
╚═══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

# Add src to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

console = Console()

BANNER = """[bold red]
    _    _____ ____ ___ ____ ____ _____ ____ ___ _  _______ 
   / \  | ____/ ___|_ _/ ___/ ___|_   _|  _ \_ _| |/ / ____|
  / _ \ |  _|| |  _ | |\___ \___ \ | | | |_) | || ' /|  _|  
 / ___ \| |__| |_| || | ___) |__) || | |  _ <| || . \| |___ 
/_/   \_\_____\____|___|____/____/ |_| |_| \_\___|_|\_\_____|
[/bold red]
[white border]Elite Reconnaissance & Automated Pentesting Framework[/white border]
"""

def display_legal_disclaimer():
    disclaimer = """[bold yellow]╔═══════════════════════════════════════════════════════════════════╗
║  ⚠️  LEGAL NOTICE - READ CAREFULLY  ⚠️                          ║
║                                                                  ║
║  AegisStrike is for EDUCATIONAL and AUTHORIZED testing only.    ║
║  Only scan systems you own or have permission to test.          ║
║                                                                  ║
║  By using this tool you agree to:                               ║
║    • Only scan authorized targets                               ║
║    • Comply with all laws                                       ║
║    • Accept full responsibility                                 ║
║                                                                  ║
║  The authors assume NO LIABILITY for misuse.                    ║
╚═══════════════════════════════════════════════════════════════════╝[/bold yellow]"""
    console.print(disclaimer)
    
    if not Confirm.ask("Do you agree to these terms?"):
        console.print("[red]You must accept the terms to use AegisStrike. Exiting.[/red]")
        sys.exit(1)

@click.command()
@click.option('-t', '--target', required=True, help='Target domain, IP, or CIDR')
@click.option('--mode', type=click.Choice(['full', 'quick', 'web', 'subdomains', 'ports', 'bugbounty', 'passive']), default='full', help='Scan mode')
@click.option('--report', type=click.Choice(['html', 'json', 'csv', 'all', 'none']), default='html', help='Report format')
@click.option('--threads', type=int, default=10, help='Number of threads')
@click.option('--timeout', type=int, default=30, help='Timeout in seconds')
@click.option('--wordlist', type=click.Path(exists=True), help='Custom wordlist path')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
@click.option('--no-active', is_flag=True, help='Forces passive-only mode')
def main(target, mode, report, threads, timeout, wordlist, verbose, no_active):
    """AegisStrike CLI Entry Point"""
    console.print(BANNER)
    display_legal_disclaimer()
    
    if no_active:
        mode = 'passive'
        console.print("[yellow][*] Active scanning disabled. Forcing passive mode.[/yellow]")

    console.print(f"\n[cyan][*] Target:[/cyan] {target}")
    console.print(f"[cyan][*] Mode:[/cyan] {mode}")
    console.print(f"[cyan][*] Report:[/cyan] {report}")
    
    try:
        from core.engine import ReconEngine
        engine = ReconEngine(target, mode, report, threads, timeout, wordlist, verbose)
        engine.run()
    except Exception as e:
        console.print(f"[red][!] Error during execution: {str(e)}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    main()
