from dnslib.server import DNSServer, BaseResolver
from dnslib import RR, QTYPE, A
import socket

from engine.evaluate import evaluate
from engine.evaluate import normalize_domain


def forward_request(request):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(request.pack(), ("8.8.8.8", 53))
    data, _ = sock.recvfrom(1024)
    return data


class AdblockResolver(BaseResolver):

    def resolve(self, request, handler):
        print("RECEIVED REQUEST")
        domain = normalize_domain(str(request.q.qname))
        print(f"Query: {domain}")
        result = evaluate(domain)

        if result == "block":
            print(f"Blocked: {domain}")
            return self.block_response(request)
        else:
            print(f"Good: {domain}")
            return forward_request(request)

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

if __name__ == "__main__":
    resolver = AdblockResolver()

    server = DNSServer(resolver, port=5353, address="127.0.0.1")
    print("Listening on port 5353")

    server.start()