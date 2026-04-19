import json
from dataclasses import dataclass
import logging


@dataclass
class Rule:
    type: str  # block/allow
    domain: str


def parse_rules():
    rules = []
    logging.info("LOADING RULES")

    with open("data/rules.json") as f:
        json_rules = json.load(f)

    for json_rule in json_rules:
        rules.append(Rule(json_rule["type"], json_rule["domain"]))

    return rules
