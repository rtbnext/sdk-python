from dataclasses import dataclass

@dataclass( slots= True, frozen= True )
class RateLimiterOptions:
  """Options for the rate limiter."""
  max_requests: int
  per_ms: int
