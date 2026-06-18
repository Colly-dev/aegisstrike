"""
AegisStrike - Attack Surface Risk Scoring
Phase: Attack Surface Analysis
EDUCATIONAL PURPOSES and AUTHORIZED SECURITY TESTING ONLY.
"""

from typing import dict as Dict

SEVERITY_WEIGHTS = {"critical": 10, "high": 7, "medium": 4, "low": 2, "info": 0}

def calculate_score(results: dict) -> dict:
    """Calculate overall attack surface risk score from scan results."""
    total_score = 0
    findings_by_severity = {"critical": [], "high": [], "medium": [], "low": [], "info": []}
    
    # Score open ports
    ports = results.get("ports", {}).get("open_ports", [])
    risky_ports = {21: "FTP", 23: "Telnet", 3389: "RDP", 5432: "PostgreSQL", 27017: "MongoDB"}
    for p in ports:
        port_num = p.get("port")
        if port_num in risky_ports:
            findings_by_severity["high"].append(f"Risky port open: {port_num} ({risky_ports[port_num]})")
            total_score += SEVERITY_WEIGHTS["high"]
        else:
            total_score += SEVERITY_WEIGHTS["low"]
    
    # Score vulnerability findings
    vulns = results.get("vulns", {})
    for check_name, check_data in vulns.items():
        if isinstance(check_data, dict):
            for finding in check_data.get("findings", check_data.get("missing", check_data.get("found", []))):
                if isinstance(finding, dict):
                    sev = finding.get("severity", "info")
                    findings_by_severity[sev].append(f"{check_name}: {finding.get('type', finding.get('header', str(finding)))}")
                    total_score += SEVERITY_WEIGHTS.get(sev, 0)
    
    # Risk level
    if total_score >= 50:
        risk_level = "CRITICAL"
    elif total_score >= 30:
        risk_level = "HIGH"
    elif total_score >= 15:
        risk_level = "MEDIUM"
    elif total_score > 0:
        risk_level = "LOW"
    else:
        risk_level = "MINIMAL"
    
    return {
        "score": total_score,
        "risk_level": risk_level,
        "findings_by_severity": findings_by_severity,
        "total_findings": sum(len(v) for v in findings_by_severity.values()),
    }
