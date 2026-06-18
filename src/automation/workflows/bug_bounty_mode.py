"""
AegisStrike - Bug Bounty Optimized Workflow
Phase: Automation
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
WARNING: Only use on targets in scope of an authorized bug bounty program.
"""

from rich.console import Console

console = Console()

def run(target: str, config: dict = None) -> dict:
    """Execute bug bounty optimized workflow focusing on high-value findings."""
    results = {}
    console.print(f"[cyan][*] Bug bounty mode started for {target}[/cyan]")
    
    # Passive recon
    try:
        from reconnaissance.passive import crtsh_enum, google_dorks
        results["crtsh"] = crtsh_enum.run(target)
        results["dorks"] = google_dorks.run(target)
    except Exception as e:
        results["passive_error"] = str(e)
    
    # Subdomain takeover
    try:
        from reconnaissance.subdomains import dns_bruteforce, takeover_detection
        subs = dns_bruteforce.run(target)
        results["subdomains"] = subs
        if subs.get("found"):
            sub_list = [s["subdomain"] for s in subs["found"]]
            results["takeover"] = takeover_detection.run(sub_list)
    except Exception as e:
        results["subdomain_error"] = str(e)
    
    # Vulnerability checks
    try:
        from vulnerability_checks.web import security_headers, cors_checker, exposed_panels
        results["headers"] = security_headers.run(target)
        results["cors"] = cors_checker.run(target)
        results["panels"] = exposed_panels.run(target)
    except Exception as e:
        results["vuln_error"] = str(e)
    
    return results
