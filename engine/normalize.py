from urllib.parse import urlparse


def normalize_domain(domain):
    if not domain.startswith(("http://", "https://")):
        domain = "http://" + domain

    parsed = urlparse(domain)

    host = parsed.netloc.lower().replace("www.", "").rstrip(".")

    return host