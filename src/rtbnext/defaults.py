"""
Defaults

Declares default values for options.
"""

from rtbnext.core.rate_limiter import RateLimitMode
from rtbnext.core.resource import CacheMode, CacheType

DEFAULT_API_URL: str = "https://api.rtbnext.de"

DEFAULT_MAX_REQUESTS: int = 60
DEFAULT_PER_SECONDS: float = 10.0
DEFAULT_RATE_LIMIT_MODE: RateLimitMode = "burst"

DEFAULT_TIMEOUT: float = 30.0

DEFAULT_CACHE_TYPE: CacheType = "memory"
DEFAULT_CACHE_MODE: CacheMode = "ttl"
