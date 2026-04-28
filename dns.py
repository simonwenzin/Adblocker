from dnslib.server import DNSServer, BaseResolver
from dnslib import RR, QTYPE, A, DNSRecord
import socket
import logging

from engine.evaluate import DomainEvaluator
from engine.normalize import normalize_domain
from engine.rules import parse_rules, parse_blockrules


class AdblockResolver(BaseResolver):

    def __init__(self):
        self.evaluator = DomainEvaluator(parse_rules(), parse_blockrules())
        self.logger = logging.getLogger(__name__)

    def resolve(self, request, handler):
        self.logger.info("Resolving request.")

        domain = str(request.q.qname)
        self.logger.info(f"Query: {domain} ({QTYPE[request.q.qtype]})")

        prel_result = self.evaluator.evaluate_domain(domain)

        if prel_result == "allow":
            domain = normalize_domain(domain)
            result = self.evaluator.evaluate(domain)
            if result == "allow":
                return self.allow_domain(domain, request)
            else:
                return self.block_domain(domain, request)
        else:
            return self.block_domain(domain, request)

    def block_response(self, request):
        reply = request.reply()
        reply.add_answer(
            RR(
                request.q.qname,
                QTYPE.A,
                rdata=A("0.0.0.0"),
                ttl=60
            )
        )
        return reply

    def forward(self, request):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)

        try:
            sock.sendto(request.pack(), ("8.8.8.8", 53))
            data, _ = sock.recvfrom(4096)
            return DNSRecord.parse(data)
        except Exception as e:
            self.logger.error("Forward error:", e)
            return self.block_response(request)

    def block_domain(self, domain, request):
        self.logger.info(f"Blocked: {domain}")
        return self.block_response(request)

    def allow_domain(self, domain, request):
        self.logger.info(f"Good: {domain}")
        return self.forward(request)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    server = DNSServer(AdblockResolver(), port=5353, address="127.0.0.1")
    server.start()
