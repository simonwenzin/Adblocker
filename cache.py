import time

from cachetools import LRUCache


class CacheEntry:

    def __init__(self, rule, ttl):
        self.rule = rule
        self.expires_at = time.time() + ttl

    def is_expired(self):
        return self.expires_at < time.time()


class DecisionCache:

    def __init__(self):
        self.cache = LRUCache(maxsize=10000)

    def get(self, domain):
        entry = self.cache.get(domain)

        if entry is None:
            return None

        if entry.is_expired():
            del self.cache[domain]
            return None

        return entry.rule

    def set(self, domain, rule):
        self.cache[domain] = CacheEntry(rule, ttl=600)
