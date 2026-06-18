"""
AegisStrike - Integration Tests: Report Engine
"""

import pytest
import os
import json
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

SAMPLE_RESULTS = {
    "passive": {"whois": {"registrar": "Test"}, "dns": {"A": ["1.2.3.4"]}},
    "ports": {"open_ports": [{"port": 80, "state": "open", "service": "http"}]},
    "vulns": {"headers": {"missing": [{"header": "CSP", "severity": "medium"}]}},
}

class TestHTMLReport:
    def test_html_report_generation(self, tmp_path):
        from core.report_engine import ReportEngine
        engine = ReportEngine(output_dir=str(tmp_path))
        engine.generate("example.com", "full", SAMPLE_RESULTS, "html")
        html_files = list(tmp_path.glob("html/*.html"))
        assert len(html_files) > 0
        content = html_files[0].read_text()
        assert "example.com" in content
        assert "AegisStrike" in content

class TestJSONReport:
    def test_json_report_generation(self, tmp_path):
        from core.report_engine import ReportEngine
        engine = ReportEngine(output_dir=str(tmp_path))
        engine.generate("example.com", "full", SAMPLE_RESULTS, "json")
        json_files = list(tmp_path.glob("json/*.json"))
        assert len(json_files) > 0
        data = json.loads(json_files[0].read_text())
        assert data["target"] == "example.com"

class TestCSVReport:
    def test_csv_report_generation(self, tmp_path):
        from core.report_engine import ReportEngine
        engine = ReportEngine(output_dir=str(tmp_path))
        engine.generate("example.com", "full", SAMPLE_RESULTS, "csv")
        csv_files = list(tmp_path.glob("csv/*.csv"))
        assert len(csv_files) > 0
