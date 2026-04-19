from engine.match import simple_match
from engine.normalize import normalize_domain


class DomainEvaluator:

    def __init__(self, rules):
        self.rules = rules

    def evaluate(self, domain):
        for rule in self.rules:
            match = simple_match(normalize_domain(domain), rule.domain)
            if match:
                if rule.type == "block":
                    return "block"
            else:
                continue
        return "allow"
