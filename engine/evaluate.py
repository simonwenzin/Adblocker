from engine.normalize import normalize_domain


class DomainEvaluator:

    def __init__(self, rules, domain_rules):
        self.rules = rules
        self.domain_rules = domain_rules

    def evaluate(self, domain):
        for rule in self.rules:
            if rule.domain in normalize_domain(domain):
                if rule.type == "block":
                    return "block"
            else:
                continue
        return "allow"

    def evaluate_domain(self, domain):
        for rule in self.domain_rules:
            if rule.domain in domain:
                if rule.type == "block":
                    return "block"
                else:
                    continue
        return "allow"
