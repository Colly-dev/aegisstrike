"""
AegisStrike - Unit Tests: Fingerprinting Modules
"""

import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

class TestCMSDetector:
    @patch('requests.get')
    def test_wordpress_detection(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "<html>wp-content/themes/default</html>"
        mock_resp.headers = {}
        mock_get.return_value = mock_resp
        from fingerprinting.web.cms_detector import run
        result = run("example.com")
        assert any(d["cms"] == "WordPress" for d in result["detected"])

    @patch('requests.get')
    def test_no_cms_detected(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "<html>Hello World</html>"
        mock_resp.headers = {}
        mock_get.return_value = mock_resp
        from fingerprinting.web.cms_detector import run
        result = run("example.com")
        assert isinstance(result["detected"], list)

class TestWAFDetector:
    @patch('requests.get')
    def test_cloudflare_detection(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = ""
        mock_resp.headers = {"CF-RAY": "abc123", "Server": "cloudflare"}
        mock_get.return_value = mock_resp
        from fingerprinting.web.waf_detector import run
        result = run("example.com")
        assert any(d["waf"] == "Cloudflare" for d in result["detected"])

class TestSecurityHeaders:
    @patch('requests.get')
    def test_missing_headers(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {"Content-Type": "text/html"}
        mock_get.return_value = mock_resp
        from vulnerability_checks.web.security_headers import run
        result = run("example.com")
        assert len(result["missing"]) > 0
