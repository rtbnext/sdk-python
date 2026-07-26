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

  def _process_queue ( self ) -> None:
    """Process waiting requests while tokens are available."""

    while self._tokens > 0 and self._queue:
      self._tokens -= 1

      future = self._queue.popleft()

      if not future.done():
        future.set_result( None )

  async def _burst_refill ( self ) -> None:
    """Refill all tokens after the configured interval."""

    await asyncio.sleep( self._options.per_ms / 1000 )

    self._tokens = self._options.max_requests
    self._task = None
    self._process_queue()
