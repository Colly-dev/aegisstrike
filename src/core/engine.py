"""
AegisStrike - Core Engine
Orchestrates the reconnaissance and scanning phases.

LEGAL NOTICE: AegisStrike is for EDUCATIONAL and AUTHORIZED testing only.
Only scan systems you own or have permission to test.
"""

import time
from rich.console import Console
from rich.table import Table

console = Console()

class ReconEngine:
    def __init__(self, target, mode, report_format, threads, timeout, wordlist, verbose):
        self.target = target
        self.mode = mode
        self.report_format = report_format
        self.threads = threads
        self.timeout = timeout
        self.wordlist = wordlist
        self.verbose = verbose
        self.start_time = None
        self.end_time = None
        self.results = {}

    def run(self):
        self.start_time = time.time()
        console.print(f"\n[bold green][+] Starting scan against {self.target} in {self.mode} mode...[/bold green]\n")
        
        with console.status("[bold cyan]Initializing engine...[/bold cyan]") as status:
            time.sleep(1)
            
            if self.mode in ['full', 'passive', 'subdomains', 'bugbounty']:
                status.update("[bold cyan]Running Passive Reconnaissance...[/bold cyan]")
                self.results['passive'] = self._run_passive()
                
            if self.mode in ['full', 'subdomains', 'bugbounty']:
                status.update("[bold cyan]Running Subdomain Enumeration...[/bold cyan]")
                self.results['subdomains'] = self._run_subdomains()
                
            if self.mode not in ['passive']:
                if self.mode in ['full', 'ports', 'bugbounty']:
                    status.update("[bold cyan]Running Active Recon & Port Scanning...[/bold cyan]")
                    self.results['ports'] = self._run_ports()
                    
                if self.mode in ['full', 'web', 'bugbounty']:
                    status.update("[bold cyan]Running Web Enumeration...[/bold cyan]")
                    self.results['web'] = self._run_web()
                    
                if self.mode in ['full', 'web', 'bugbounty']:
                    status.update("[bold cyan]Running Fingerprinting & Vulnerability Checks...[/bold cyan]")
                    self.results['vulns'] = self._run_vulns()
                    
            status.update("[bold cyan]Generating Reports...[/bold cyan]")
            self._generate_reports()
            
        self.end_time = time.time()
        self._print_summary()

    def _run_passive(self):
        time.sleep(1)
        return {"whois": "completed", "dns": "completed"}

    def _run_subdomains(self):
        time.sleep(1)
        return {"found": 5}

    def _run_ports(self):
        time.sleep(1)
        return {"open_ports": [80, 443]}

    def _run_web(self):
        time.sleep(1)
        return {"directories": 12}

    def _run_vulns(self):
        time.sleep(1)
        return {"findings": 3}

    def _generate_reports(self):
        time.sleep(1)
        
    def _print_summary(self):
        duration = round(self.end_time - self.start_time, 2)
        console.print(f"\n[bold green][+] Scan completed in {duration} seconds.[/bold green]")
        
        table = Table(title="Scan Summary")
        table.add_column("Phase", style="cyan")
        table.add_column("Status/Results", style="green")
        
        for phase, result in self.results.items():
            table.add_row(phase.capitalize(), str(result))
            
        console.print(table)
