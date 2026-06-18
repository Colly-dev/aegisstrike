# AegisStrike Architecture

## Overview

AegisStrike is organized as a modular Python framework with clearly separated concerns across reconnaissance, enumeration, fingerprinting, vulnerability assessment, and reporting layers.

## Component Diagram

```
aegisstrike.py (CLI Entry Point)
        │
        ▼
src/core/engine.py (Orchestrator)
        │
        ├── src/reconnaissance/
        │   ├── passive/     (WHOIS, DNS, crt.sh, Google Dorks, GitHub)
        │   ├── active/      (Host Discovery, Banner Grabbing)
        │   └── subdomains/  (DNS Bruteforce, Permutation, Takeover)
        │
        ├── src/enumeration/
        │   ├── ports/       (nmap / socket fallback)
        │   ├── web/         (gobuster / requests fallback, robots.txt)
        │   ├── ssl/         (SSL/TLS checker)
        │   └── dns/         (Zone transfer)
        │
        ├── src/fingerprinting/
        │   ├── web/         (CMS, WAF detection)
        │   └── infrastructure/ (Cloud/CDN detection)
        │
        ├── src/vulnerability_checks/
        │   ├── web/         (Headers, CORS, Exposed Panels)
        │   ├── infrastructure/ (Weak SSL)
        │   └── cloud/       (Open S3 Buckets)
        │
        ├── src/intelligence/
        │   ├── cve_mapping/ (NVD API CVE lookup)
        │   └── enrichment/  (Geolocation, ASN)
        │
        ├── src/attack_surface/
        │   └── risk_scoring.py (Risk calculation)
        │
        └── src/core/report_engine.py (HTML/JSON/CSV reports)
```

## Scan Modes

| Mode       | Description                              |
|------------|------------------------------------------|
| full       | All phases in sequence                   |
| quick      | Fast scan of key indicators              |
| web        | Web enumeration and fingerprinting only  |
| subdomains | Subdomain enumeration only               |
| ports      | Port scanning only                       |
| bugbounty  | Bug bounty optimized workflow            |
| passive    | Passive recon only (no target contact)   |
