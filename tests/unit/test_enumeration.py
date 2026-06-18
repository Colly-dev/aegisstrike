"""
AegisStrike - Unit Tests: Enumeration Modules
"""

import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

class TestPortScanner:
    @patch('socket.socket')
    def test_socket_scan_open_port(self, mock_socket):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 0
        mock_socket.return_value = mock_sock
        from enumeration.ports.nmap_scan import _socket_scan
        results = _socket_scan("127.0.0.1", [80], timeout=1)
        assert len(results) > 0
        assert results[0]["state"] == "open"

    @patch('socket.socket')
    def test_socket_scan_closed_port(self, mock_socket):
        mock_sock = MagicMock()
        mock_sock.connect_ex.return_value = 1
        mock_socket.return_value = mock_sock
        from enumeration.ports.nmap_scan import _socket_scan
        results = _socket_scan("127.0.0.1", [9999], timeout=1)
        assert len(results) == 0

class TestRobotsParser:
    @patch('requests.get')
    def test_robots_parsing(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = "User-agent: *\nDisallow: /admin\nAllow: /\nSitemap: https://example.com/sitemap.xml"
        mock_get.return_value = mock_resp
        from enumeration.web.robots_parser import run
        result = run("example.com")
        assert "/admin" in result["disallowed"]
        assert "https://example.com/sitemap.xml" in result["sitemaps"]

class TestSSLChecker:
    @patch('ssl.create_default_context')
    def test_ssl_error_handling(self, mock_ctx):
        mock_ctx.side_effect = Exception("SSL error")
        from enumeration.ssl.ssl_checker import run
        result = run("example.com")
        assert "error" in result or "target" in result
