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
