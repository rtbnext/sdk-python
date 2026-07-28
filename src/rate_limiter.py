"""
Rate Limiter

Implements a rate limiter supporting burst and spread strategies.

Supports two strategies:
- `burst`: allows short bursts of requests
- `spread`: distributes requests evenly over time
"""

from __future__ import annotations

import asyncio
from collections import deque
from time import monotonic


class RateLimiter:
    """Async rate limiter supporting burst and spread strategies."""

    def __init__ ( self, max_requests: int, per_ms: int ) -> None:
        self._max_requests = max_requests
        self._per_seconds = per_ms / 1000
        self._interval = self._per_seconds / max_requests

        self._burst = deque[ float ]()
        self._next_allowed = 0.0

        self._lock = asyncio.Lock()
