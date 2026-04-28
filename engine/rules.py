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


def parse_blockrules():
    blocked_domains = []
    logging.info("LOADING BLOCKED DOMAINS")

    with open("data/ads.txt") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split(" ")
            domain = parts[1]
            blocked_domains.append(Rule("block", domain))

    return blocked_domains
