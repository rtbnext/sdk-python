"""
Defaults

Declares default values for options.
"""

from rtbnext.core.rate_limiter import RateLimitMode

DEFAULT_RATE_LIMIT_MODE: RateLimitMode = "burst"
DEFAULT_TIMEOUT: float = 30.0
