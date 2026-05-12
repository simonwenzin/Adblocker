from unittest.mock import Mock

from engine.evaluate import DomainEvaluator


class FakeRule:
    def __init__(self, type, domain):
        self.type = type
        self.domain = domain


def test_evaluate_domain_blocks_matching_domain():
    domain_rules = [FakeRule("block", "example.com")]

    evaluator = DomainEvaluator(rules=[], domain_rules=domain_rules)

    result = evaluator.evaluate_domain("example.com")

    assert result == "block"


def test_evaluate_domain_falls_back_to_evaluate():
    domain_rules = [FakeRule("allow", "youtube.com")]

    evaluator = DomainEvaluator(rules=[], domain_rules=domain_rules)
    evaluator._evaluate = Mock(return_value="allow")

    evaluator.evaluate_domain("youtube.com")

    evaluator._evaluate.assert_called_once_with("youtube.com")


def test_evaluate_blocks_matching_domain():
    rules = [FakeRule("block", "example.com")]

    evaluator = DomainEvaluator(rules=rules, domain_rules=[])

    result = evaluator._evaluate("example.com")

    assert result == "block"


def test_evaluate_allows_non_matching_domain():
    domain_rules = [FakeRule("block", "example.com")]

    evaluator = DomainEvaluator(rules=[], domain_rules=domain_rules)

    result = evaluator.evaluate_domain("youtube.com")

    assert result == "allow"
