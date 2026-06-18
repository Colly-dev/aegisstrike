"""
AegisStrike - Full Reconnaissance Workflow
Phase: Automation
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
WARNING: This workflow performs active scanning. Only use on authorized targets.
"""

from rich.console import Console

console = Console()

def run(target: str, config: dict = None) -> dict:
    """Execute the full reconnaissance workflow."""
    results = {}
    console.print(f"[cyan][*] Full recon workflow started for {target}[/cyan]")
    
    # Passive
    try:
        from reconnaissance.passive import whois_lookup, dns_lookup, crtsh_enum
        results["whois"] = whois_lookup.run(target)
        results["dns"] = dns_lookup.run(target)
        results["crtsh"] = crtsh_enum.run(target)
    except Exception as e:
        results["passive_error"] = str(e)
    
    # Subdomains
    try:
        from reconnaissance.subdomains import dns_bruteforce
        results["subdomains"] = dns_bruteforce.run(target)
    except Exception as e:
        results["subdomain_error"] = str(e)
    
    # Ports
    try:
        from enumeration.ports import nmap_scan
        results["ports"] = nmap_scan.run(target)
    except Exception as e:
        results["port_error"] = str(e)
    
    # Web
    try:
        from enumeration.web import robots_parser, gobuster_runner
        results["robots"] = robots_parser.run(target)
        results["directories"] = gobuster_runner.run(target)
    except Exception as e:
        results["web_error"] = str(e)
    
    return results
