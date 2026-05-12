from engine.normalize import normalize_domain


def test_normalize_domain_removes_www():
    domain = "http://www.example.com"

    result = normalize_domain(domain)

    assert result == "example.com"


def test_normalize_domain_adds_missing_protocol():
    domain = "example.com"

    result = normalize_domain(domain)

    assert result == "example.com"


def test_normalize_domain_removes_path():
    domain = "http://example.com/examplepage"

    result = normalize_domain(domain)

    assert result == "example.com"


def test_normalize_domain_lowercases():
    domain = "http://WWW.EXAMPLE.COM"

    result = normalize_domain(domain)

    assert result == "example.com"


def test_normalize_domain_removes_trailing_dot():
    domain = "http://www.example.com."

    result = normalize_domain(domain)

    assert result == "example.com"


def test_normalize_domain_removes_trailing_slash():
    domain = "http://www.example.com/"

    result = normalize_domain(domain)

    assert result == "example.com"
