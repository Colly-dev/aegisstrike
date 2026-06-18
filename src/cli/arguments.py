"""
AegisStrike - CLI Arguments
Defines the command-line interface using Click.
"""

import click

SCAN_MODES = ['full', 'quick', 'web', 'subdomains', 'ports', 'bugbounty', 'passive']
REPORT_FORMATS = ['html', 'json', 'csv', 'all', 'none']

def get_cli_options():
    """Return Click decorators for CLI options."""
    return [
        click.option('-t', '--target', required=True, help='Target domain, IP, or CIDR'),
        click.option('--mode', type=click.Choice(SCAN_MODES), default='full', show_default=True, help='Scan mode'),
        click.option('--report', type=click.Choice(REPORT_FORMATS), default='html', show_default=True, help='Report format'),
        click.option('--threads', type=int, default=10, show_default=True, help='Number of threads'),
        click.option('--timeout', type=int, default=30, show_default=True, help='Timeout in seconds'),
        click.option('--wordlist', type=click.Path(exists=True), help='Custom wordlist path'),
        click.option('-v', '--verbose', is_flag=True, help='Enable verbose output'),
        click.option('--no-active', is_flag=True, help='Force passive-only mode'),
    ]
