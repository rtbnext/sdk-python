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
from typing import Literal

from rtbnext.defaults import DEFAULT_MAX_REQUESTS, DEFAULT_PER_SECONDS

type RateLimitMode = Literal[ "burst", "spread" ]


class RateLimiter:
    """
    Rate limitting API requests.
    
    Async rate limiter supporting burst and spread strategies:
    - `burst`: allows short bursts of requests
    - `spread`: distributes requests evenly over time
    """

    def __init__(
        self,
        max_requests: int = DEFAULT_MAX_REQUESTS,
        per_seconds: float = DEFAULT_PER_SECONDS
    ) -> None:
        self._max_requests, self._per_seconds = max_requests, per_seconds
        self._interval = self._per_seconds / max_requests

        self._burst = deque[ float ]()
        self._next_allowed = 0.0

        self._lock = asyncio.Lock()

    async def _spread_refill( self ) -> None:
        """Wait until the next evenly distributed request is allowed."""

        async with self._lock:
            now = monotonic()
            self._next_allowed = max( self._next_allowed, now )
            wait = self._next_allowed - now
            self._next_allowed += self._interval

        if wait > 0:
            await asyncio.sleep( wait )

    async def burst( self ) -> None:
        """
        Allow up to max_requests immediately.
        Further requests wait until the rolling window expires.
        """

        while True:
            async with self._lock:
                now = monotonic()

                while self._burst and now - self._burst[ 0 ] >= self._per_seconds:
                    self._burst.popleft()

                if len( self._burst ) < self._max_requests:
                    self._burst.append( now )
                    return

                wait = self._per_seconds - ( now - self._burst[ 0 ] )

            await asyncio.sleep( wait )
