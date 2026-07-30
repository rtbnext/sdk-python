"""
Defaults

Declares default values for options.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rtbnext.core.rate_limiter import RateLimitMode

DEFAULT_API_URL: str = "https://api.rtbnext.de"

DEFAULT_MAX_REQUESTS: int = 60
DEFAULT_PER_SECONDS: float = 10.0
DEFAULT_RATE_LIMIT_MODE: RateLimitMode = "burst"
