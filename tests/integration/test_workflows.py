"""
AegisStrike - Integration Tests: Workflows
"""

import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

class TestRiskScoring:
    def test_risk_scoring_with_open_ports(self):
        from attack_surface.risk_scoring import calculate_score
        results = {
            "ports": {"open_ports": [{"port": 21, "state": "open"}, {"port": 80, "state": "open"}]},
            "vulns": {}
        }
        score = calculate_score(results)
        assert "score" in score
        assert "risk_level" in score
        assert score["score"] > 0

    def test_risk_scoring_empty(self):
        from attack_surface.risk_scoring import calculate_score
        score = calculate_score({})
        assert score["risk_level"] == "MINIMAL"

class TestTargetManager:
    def test_domain_parsing(self):
        from core.target_manager import TargetManager
        tm = TargetManager("example.com")
        assert tm.is_domain is True
        assert tm.host == "example.com"

    def test_ip_parsing(self):
        from core.target_manager import TargetManager
        tm = TargetManager("192.168.1.1")
        assert tm.is_ip is True

    def test_invalid_target(self):
        from core.target_manager import TargetManager
        tm = TargetManager("not_a_valid_target!!!")
        assert tm.is_valid() is False
