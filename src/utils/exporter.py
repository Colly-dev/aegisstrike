"""
AegisStrike - Exporter
Data export utilities for CSV, JSON, and HTML formats.
"""

import json
import csv
import os
from datetime import datetime

def to_json(data: dict, output_path: str = None) -> str:
    """Export data to JSON format."""
    json_str = json.dumps(data, indent=2, default=str)
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(json_str)
    return json_str

def to_csv(data: dict, output_path: str = None) -> str:
    """Export data to CSV format."""
    rows = []
    for key, value in data.items():
        if isinstance(value, list):
            for item in value:
                rows.append({"category": key, "data": str(item)})
        else:
            rows.append({"category": key, "data": str(value)})
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["category", "data"])
            writer.writeheader()
            writer.writerows(rows)
    return str(rows)

def to_html(data: dict, target: str, output_path: str = None) -> str:
    """Export data to a simple HTML report."""
    html = f"<html><body><h1>AegisStrike Report - {target}</h1><pre>{json.dumps(data, indent=2, default=str)}</pre></body></html>"
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(html)
    return html
