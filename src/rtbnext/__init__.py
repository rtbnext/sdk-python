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
from rtbnext.core.http_client import ClientIdentity
from rtbnext.core.resource import CacheMode, CacheType
from rtbnext.defaults import (
    DEFAULT_API_URL, DEFAULT_CACHE_MODE, DEFAULT_CACHE_TYPE, DEFAULT_TIMEOUT
)
from rtbnext.rtbnext import RTBNext


def rtbnext(
    client: ClientIdentity, *,
    base_url: str = DEFAULT_API_URL,
    timeout: float = DEFAULT_TIMEOUT,
    cache: CacheType = DEFAULT_CACHE_TYPE,
    mode: CacheMode = DEFAULT_CACHE_MODE
) -> RTBNext:
    """
    Creates a new RTBNext SDK instance.

    Args:
        client: Client identity information.
        base_url: RTBNext API base URL.
        timeout: HTTP request timeout.
        cache: Cache implementation.
        mode: Cache mode.

    Returns:
        A configured RTBNext SDK instance.
    """

    return RTBNext(
        client, base_url= base_url, timeout= timeout,
        cache= cache, mode= mode
    )


__all__ = [
    "RTBNext",
    "ClientIdentity",
    "CacheType",
    "CacheMode",
    "rtbnext"
]
