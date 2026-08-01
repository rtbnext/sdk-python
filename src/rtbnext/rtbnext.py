"""
RTBNext

Implements the main entry point class for the RTBNext Python SDK exposing
all API endpoints.
"""

from __future__ import annotations

from typing import Any

from rtbnext.core.http_client import ClientIdentity, HttpClient
from rtbnext.core.loader import CacheMode, CacheType, ResourceStateLoader
from rtbnext.defaults import DEFAULT_API_URL, DEFAULT_CACHE_MODE, DEFAULT_CACHE_TYPE
from rtbnext.endpoint.system import SystemEndpoint
from rtbnext.resource.base import ResourcePool


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
        cache: CacheType = DEFAULT_CACHE_TYPE,
        mode: CacheMode = DEFAULT_CACHE_MODE,
        timeout: float | None = None
    ) -> None:
        ...
