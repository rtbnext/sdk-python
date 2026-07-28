"""
Rate Limiter

Implements a token-based rate limiter with support for burst and spread strategies.

Supports two strategies:
- `burst`: allows short bursts of requests
- `spread`: distributes requests evenly over time
"""

from __future__ import annotations

import asyncio
from collections import deque


class RateLimiter:
    """Token-based rate limiter."""

    def __init__ ( self, max_requests: int, per_ms: int ) -> None:
        self._max_requests = max_requests
        self._per_ms = per_ms

        self._tokens = max_requests
        self._refill_interval = per_ms / max_requests / 1000
        self._queue: deque[ asyncio.Future[ None ] ] = deque()
        self._task: asyncio.Task[ None ] | None = None

    def _process_queue ( self ) -> None:
        """Process waiting requests while tokens are available."""

        while self._tokens > 0 and self._queue:
            self._tokens -= 1

            future = self._queue.popleft()
            if not future.done():
                future.set_result( None )
