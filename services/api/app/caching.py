"""
Cache implementation with Redis and local fallback options.
"""

import os
import time
import pickle
from typing import Any, Optional, Tuple

try:
    import redis  # type: ignore
except Exception:
    redis = None


class Cache:
    def __init__(
        self,
        backend: str,
        ttl_seconds: int,
        redis_url: str | None = None,
        local_pickle_path: str | None = None,
    ):
        self.backend = backend
        self.ttl = ttl_seconds
        self.local_pickle_path = local_pickle_path
        self.mem = {}  # key -> (value, expire_ts)
        self.r = None
        if backend == "redis" and redis and redis_url:
            self.r = redis.from_url(redis_url)
        elif backend == "redis" and not redis:
            print(
                "[cache] redis backend requested but redis lib not installed; falling back to local"
            )
            self.backend = "local"
        # Load persisted local cache if exists
        if (
            self.backend == "local"
            and self.local_pickle_path
            and os.path.exists(self.local_pickle_path)
        ):
            try:
                with open(self.local_pickle_path, "rb") as f:
                    self.mem = pickle.load(f)
            except Exception:
                self.mem = {}

    def _persist_local(self):
        if self.backend == "local" and self.local_pickle_path:
            os.makedirs(os.path.dirname(self.local_pickle_path), exist_ok=True)
            with open(self.local_pickle_path, "wb") as f:
                pickle.dump(self.mem, f)

    def make_key(
        self,
        model_id: str,
        prompt: str,
        tools_signature: str = "",
        mode: str = "",
        version_tag: str = "",
    ) -> str:
        # Keep it simple; you can hash if you prefer
        base = f"m={model_id}|mode={mode}|ver={version_tag}|tools={tools_signature}|p={prompt}"
        # Optional: hash long keys
        if len(base) > 512:
            import hashlib

            return hashlib.sha256(base.encode("utf-8")).hexdigest()
        return base

    def get(self, key: str) -> Optional[Tuple[Any, dict]]:
        now = time.time()
        if self.backend == "redis" and self.r:
            raw = self.r.get(key)
            if not raw:
                return None
            value, meta, expire_ts = pickle.loads(raw)
            if expire_ts and expire_ts < now:
                self.r.delete(key)
                return None
            return value, meta

        # local
        slot = self.mem.get(key)
        if not slot:
            return None
        value, meta, expire_ts = slot
        if expire_ts and expire_ts < now:
            self.mem.pop(key, None)
            self._persist_local()
            return None
        return value, meta

    def set(self, key: str, value: Any, meta: dict | None = None):
        expire_ts = time.time() + self.ttl if self.ttl else None
        meta = meta or {}
        if self.backend == "redis" and self.r:
            payload = pickle.dumps((value, meta, expire_ts))
            self.r.set(key, payload, ex=self.ttl if self.ttl else None)
            return
        self.mem[key] = (value, meta, expire_ts)
        self._persist_local()
