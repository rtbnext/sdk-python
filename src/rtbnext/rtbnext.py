"""
RTBNext

Implements the main entry point class for the RTBNext Python SDK exposing
all API endpoints.
"""

from __future__ import annotations

from dataclasses import dataclass

from rtbnext.core.http_client import ClientIdentity, HttpClient
from rtbnext.core.loader import CacheMode, CacheType, ResourceStateLoader
from rtbnext.defaults import (
    DEFAULT_API_URL, DEFAULT_CACHE_MODE, DEFAULT_CACHE_TYPE, DEFAULT_TIMEOUT
)
from rtbnext.endpoint.profile import ProfileEndpoint
from rtbnext.endpoint.stats import StatsEndpoint
from rtbnext.endpoint.system import SystemEndpoint
from rtbnext.resource.base import ResourcePool


@dataclass( slots= True, kw_only= True )
class Endpoints:
    """Endpoints available in the RTBNext SDK."""

    profile: ProfileEndpoint
    stats: StatsEndpoint
    system: SystemEndpoint


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
        self._loader = ResourceStateLoader( client= self._client, cache= cache, mode= mode )
        self._pool = ResourcePool()

        endpoint_map: dict[ str, Any ] = {}
        args = ( self._loader, self._pool, endpoint_map )

        self.profile = endpoint_map[ "profile" ] = ProfileEndpoint( *args )
        self.stats = endpoint_map[ "stats" ] = StatsEndpoint( *args )
        self.system = endpoint_map[ "system" ] = SystemEndpoint( *args )

        self.endpoints = Endpoints(
            profile= self.profile, stats= self.stats, system= self.system
        )


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
