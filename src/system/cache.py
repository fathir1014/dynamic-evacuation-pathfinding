# src/system/cache.py

class PathCache:
    def __init__(self):
        self.storage = {}

    def has(self, key):
        return key in self.storage

    def get(self, key):
        return self.storage.get(key)

    def set(self, key, path):
        self.storage[key] = path