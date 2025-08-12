# app/utils/cache.py
import time
from typing import Any, Dict, Optional

class Cache:
    def __init__(self, default_ttl: int = 120):
        self.default_ttl = default_ttl
        self._store: Dict[str, Any] = {}
        self._exp: Dict[str, float] = {}

    def get(self, key: str) -> Optional[Any]:
        exp = self._exp.get(key)
        if exp is None:
            return None
        if time.time() > exp:
            self._store.pop(key, None)
            self._exp.pop(key, None)
            return None
        return self._store.get(key)

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        ttl = self.default_ttl if ttl is None else ttl
        self._store[key] = value
        self._exp[key] = time.time() + ttl
