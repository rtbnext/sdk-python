"""
RTBNext

Implements the main entry point class for the RTBNext Python SDK exposing
all API endpoints.
"""

from __future__ import annotations

from rtbnext.core.http_client import ClientIdentity, HttpClient
from rtbnext.core.resource import CacheMode, CacheType, ResourceLoader, ResourcePool
from rtbnext.defaults import (
    DEFAULT_API_URL, DEFAULT_CACHE_MODE, DEFAULT_CACHE_TYPE, DEFAULT_TIMEOUT
)


class RTBNext:
    """
    Main entry point of the RTBNext SDK.

    Provides access to all RTBNext API endpoints through a single client
    instance while internally managing HTTP communication, resource loading,
    caching, and endpoint initialization.
    """

    def __init__(
        self, client: ClientIdentity, *,
        base_url: str = DEFAULT_API_URL,
        timeout: float = DEFAULT_TIMEOUT,
        cache: CacheType = DEFAULT_CACHE_TYPE,
        mode: CacheMode = DEFAULT_CACHE_MODE
    ) -> None:
        self._client = HttpClient( client= client, base_url= base_url, timeout= timeout )
        self._loader = ResourceLoader( client= self._client, cache= cache, mode= mode )
        self._pool = ResourcePool()
