from __future__ import annotations

import asyncio
from collections import deque
from dataclasses import dataclass


@dataclass ( slots= True, frozen= True )
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

  async def _spread_refill ( self ) -> None:
    """Continuously refill tokens one by one."""

    while True:
      await asyncio.sleep( self._refill_interval )

      if self._tokens < self._options.max_requests:
        self._tokens += 1
        self._process_queue()

      if self._tokens == self._options.max_requests and not self._queue:
        self._task = None
        return

  async def burst ( self ) -> None:
    """
    Acquire a token using burst mode.

    Allows immediate requests until the bucket is empty.
    Afterwards, requests wait until the bucket is completely refilled.
    """

    if self._tokens > 0:
      self._tokens -= 1
      return

    loop = asyncio.get_running_loop()
    future = loop.create_future()

    self._queue.append( future )

    if self._task is None:
      self._task = asyncio.create_task( self._burst_refill() )

    await future
