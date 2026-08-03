"""
RTBNext

Implements the main entry point class for the RTBNext Python SDK exposing
all API endpoints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Self

from rtbnext.core.http_client import ClientIdentity, HttpClient
from rtbnext.core.loader import CacheMode, CacheType, ResourceStateLoader
from rtbnext.defaults import (
    DEFAULT_API_URL, DEFAULT_CACHE_MODE, DEFAULT_CACHE_TYPE, DEFAULT_TIMEOUT
)
from rtbnext.endpoint.filter import FilterEndpoint
from rtbnext.endpoint.list import ListEndpoint
from rtbnext.endpoint.mover import MoverEndpoint
from rtbnext.endpoint.profile import ProfileEndpoint
from rtbnext.endpoint.stats import StatsEndpoint
from rtbnext.endpoint.system import SystemEndpoint
from rtbnext.resource.base import ResourcePool


@dataclass( slots= True, kw_only= True )
class Endpoints:
    """Endpoints available in the RTBNext SDK."""

    profile: ProfileEndpoint
    list: ListEndpoint
    mover: MoverEndpoint
    filter: FilterEndpoint
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

        endpoints = Endpoints.__new__( Endpoints )
        args = ( self._loader, self._pool, endpoints )

        self.profile = endpoints.profile = ProfileEndpoint( *args )
        self.list = endpoints.list = ListEndpoint( *args )
        self.mover = endpoints.mover = MoverEndpoint( *args )
        self.filter = endpoints.filter = FilterEndpoint( *args )
        self.stats = endpoints.stats = StatsEndpoint( *args )
        self.system = endpoints.system = SystemEndpoint( *args )

        self.endpoints = endpoints

    async def __aenter__( self ) -> Self:
        return self

    async def __aexit__( self, *_ ) -> None:
        await self.close()

    async def close( self ) -> None:
        """Closes the underlying HTTP client and release network resources."""

        await self._loader.aclose()


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
