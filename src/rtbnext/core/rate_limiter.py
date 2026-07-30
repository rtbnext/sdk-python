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
