import time

class Cache:
    def __init__(self, default_ttl=120):
        self.default_ttl = default_ttl
        self.data = {}  # store as {key: (expiry_time, value)}

    def get(self, key):
        if key in self.data:
            expiry, value = self.data[key]
            if time.time() < expiry:
                return value
            else:
                del self.data[key]
        return None

    def set(self, key, value):
        expiry_time = time.time() + self.default_ttl
        self.data[key] = (expiry_time, value)
