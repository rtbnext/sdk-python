"""
RTBNext Python SDK

Official Python SDK for the RTBNext API.

Provides access to all RTBNext API endpoints, resources, and data models.
The SDK offers lazy loading, transparent caching, automatic revalidation,
and a resource-oriented API for working with lists, profiles, filters,
statistics, and time series data.

Author: Paul Köhler (komed3)
License: MIT
"""

from rtbnext._version import __version__
from rtbnext.core.cache import Cache
from rtbnext.core.http_client import ClientIdentity
from rtbnext.core.loader import CacheMode, CacheType
from rtbnext.core.rate_limiter import RateLimitMode
from rtbnext.resource.base import ResourceEvent
from rtbnext.resource.series import AggregatePeriod
from rtbnext.rtbnext import RTBNext, rtbnext

__all__ = [
    "RTBNext",
    "rtbnext",
    "ClientIdentity",
    "RateLimitMode",
    "CacheType",
    "CacheMode",
    "ResourceEvent",
    "AggregatePeriod",
    "Cache"
]
