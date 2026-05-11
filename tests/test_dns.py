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


def test_resolve_allows_domain():
    mock_evaluator = Mock()
    mock_cache = Mock()

    mock_cache.get.return_value = None

    mock_evaluator.evaluate_domain.return_value = "allow"
    mock_evaluator.evaluate.return_value = "allow"

    resolver = AdblockResolver(evaluator=mock_evaluator, cache=mock_cache)
    resolver.forward = Mock(return_value="forwarded")

    request = DNSRecord.question("youtube.com")

    assert resolver.resolve(request, None) == "forwarded"

    mock_cache.set.assert_called_once_with("youtube.com.", "allow")


def test_allow_domain_calls_forward():
    mock_evaluator = Mock()
    mock_cache = Mock()

    mock_cache.get.return_value = None
    mock_evaluator.evaluate_domain.return_value = "allow"

    resolver = AdblockResolver(evaluator=mock_evaluator, cache=mock_cache)
    resolver.forward = Mock()

    request = DNSRecord.question("youtube.com")

    resolver.allow_domain("youtube.com", request)

    resolver.forward.assert_called_once_with(request)


def test_cache_hit_doesnt_call_evaluator():
    mock_evaluator = Mock()
    mock_cache = Mock()

    mock_cache.get.return_value = "allow"

    resolver = AdblockResolver(evaluator=mock_evaluator, cache=mock_cache)
    resolver.allow_domain = Mock()

    request = DNSRecord.question("youtube.com")
    resolver.resolve(request, None)

    mock_evaluator.evaluate_domain.assert_not_called()
    resolver.allow_domain.assert_called_once()


def test_cache_hit_allow_calls_allow_domain():
    mock_evaluator = Mock()
    mock_cache = Mock()

    mock_cache.get.return_value = "allow"

    resolver = AdblockResolver(evaluator=mock_evaluator, cache=mock_cache)
    resolver.allow_domain = Mock(return_value="allow")

    request = DNSRecord.question("youtube.com")

    assert resolver.resolve(request, None) == "allow"

    resolver.allow_domain.assert_called_once()


def test_cache_hit_block_calls_block_domain():
    mock_evaluator = Mock()
    mock_cache = Mock()

    mock_cache.get.return_value = "block"

    resolver = AdblockResolver(evaluator=mock_evaluator, cache=mock_cache)
    resolver.block_domain = Mock(return_value="block")

    request = DNSRecord.question("example.com")

    assert resolver.resolve(request, None) == "block"

    resolver.block_domain.assert_called_once()
