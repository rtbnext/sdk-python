from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass


@dataclass( slots= True, frozen= True )
class RateLimiterOptions:
  """Configuration options for the rate limiter."""

  max_requests: int
  per_ms: int


class RateLimiter:
  """
  Token-based rate limiter.

  Supports two strategies:
  - burst: allows short bursts of requests
  - spread: distributes requests evenly over time
  """

  def __init__ ( self, options: RateLimiterOptions ) -> None:
    self._options = options

    self._tokens = options.max_requests
    self._refill_interval = options.per_ms / options.max_requests / 1000

    self._queue: deque[ asyncio.Future[ None ] ] = deque()
    self._task: asyncio.Task[ None ] | None = None
