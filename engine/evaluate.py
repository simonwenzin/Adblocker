from engine.match import simple_match
from engine.normalize import normalize_domain
from engine.rules import parse_rules

def evaluate(domain):
    for rule in parse_rules():
        match = simple_match(normalize_domain(domain), rule.domain)
        if match:
            if rule.type == "block":
                return "block"
        else:
            continue
    return "allow"