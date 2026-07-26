from dataclasses import dataclass


@dataclass( slots= True, frozen= True )
class RateLimiterOptions:
  """Options for the rate limiter."""
  max_requests: int
  per_ms: int


class RateLimiter:
  """
  Token-based rate limiter for controlling request throughput.

  Supports two limiting strategies:
  - burst: allows short request bursts up to the configured limit
  - spread: distributes requests evenly over the configured interval
  """
