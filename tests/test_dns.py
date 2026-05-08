from unittest.mock import Mock

from dns import AdblockResolver
from dnslib import DNSRecord


def test_block_response_returns_0_0_0_0():
    resolver = AdblockResolver()
    request = DNSRecord.question("example.com")
    response = resolver.block_response(request)

    assert str(response.rr[0].rdata) == "0.0.0.0"

def test_resolve_blocks_domain():
    mock_evaluator = Mock()
    mock_cache = Mock()

    mock_cache.get.return_value = None
    mock_evaluator.evaluate_domain.return_value = "block"

    resolver = AdblockResolver(evaluator=mock_evaluator, cache=mock_cache)

    request = DNSRecord.question("ads.example.com")

    response = resolver.resolve(request, None)

    assert str(response.rr[0].rdata) == "0.0.0.0"

    mock_cache.set.assert_called_once_with("ads.example.com.", "block")