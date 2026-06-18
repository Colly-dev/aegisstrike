"""
AegisStrike - Unit Tests: Reconnaissance Modules
"""

import pytest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

class TestWhoisLookup:
    @patch('whois.whois')
    def test_whois_success(self, mock_whois):
        mock_whois.return_value = MagicMock(
            registrar="Test Registrar", creation_date="2020-01-01",
            expiration_date="2025-01-01", name_servers=["ns1.test.com"],
            emails=["admin@test.com"], org="Test Org"
        )
        from reconnaissance.passive.whois_lookup import run
        result = run("example.com")
        assert "registrar" in result
        assert result["registrar"] == "Test Registrar"

    @patch('whois.whois', side_effect=Exception("WHOIS failed"))
    def test_whois_failure(self, mock_whois):
        from reconnaissance.passive.whois_lookup import run
        result = run("example.com")
        assert "error" in result

class TestDnsLookup:
    @patch('dns.resolver.resolve')
    def test_dns_success(self, mock_resolve):
        mock_answer = MagicMock()
        mock_answer.__iter__ = MagicMock(return_value=iter([MagicMock(__str__=lambda s: "1.2.3.4")]))
        mock_resolve.return_value = mock_answer
        from reconnaissance.passive.dns_lookup import run
        result = run("example.com")
        assert isinstance(result, dict)

class TestGoogleDorks:
    def test_dorks_generation(self):
        from reconnaissance.passive.google_dorks import run
        result = run("example.com")
        assert "dorks" in result
        assert len(result["dorks"]) > 0
        assert all("example.com" in d for d in result["dorks"])

class TestTargetValidation:
    def test_valid_domain(self):
        from utils.validators import validate_target
        valid, ttype = validate_target("example.com")
        assert valid is True
        assert ttype == "domain"

    def test_valid_ip(self):
        from utils.validators import validate_target
        valid, ttype = validate_target("192.168.1.1")
        assert valid is True
        assert ttype == "ip"

    def test_invalid_target(self):
        from utils.validators import validate_target
        valid, ttype = validate_target("")
        assert valid is False

    def test_valid_cidr(self):
        from utils.validators import validate_target
        valid, ttype = validate_target("192.168.1.0/24")
        assert valid is True
        assert ttype == "cidr"
