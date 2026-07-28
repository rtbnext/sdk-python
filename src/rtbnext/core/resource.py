"""
Resource

Implements the resource loader and pooling of resource states.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Literal, TypeAlias
import httpx

from rtbnext.core.cache import Cache, EmptyCache, MemoryCache
from rtbnext.core.http_client import HttpClient, HttpResponse, HttpHeader, RateLimitMode

CacheType: TypeAlias = Cache | Literal[ False, "memory" ]
CachMode: TypeAlias = Literal[ "ttl", "session", "revalidate" ]


@dataclass( slots= True )
class ResourceState:
    """Represents the state of a cached resource."""

    response: HttpResponse
    created: float
    expires: float | None = None
    etag: str | None = None
    last_modified: str | None = None


class ResourceLoader:
    """
    Loads resources with optional caching and HTTP revalidation.

    The loader supports session, TTL and revalidation cache modes while
    transparently handling conditional HTTP requests.
    """

    def __init__(
        self, *,
        client: HttpClient,
        cache: CacheType = "memory",
        mode: CachMode = "ttl"
    ) -> None:
        self._client, self._mode = client, mode

        match cache:
            case False: self._cache = EmptyCache()
            case "memory": self._cache = MemoryCache()
            case _ if isinstance( cache, Cache ): self._cache = cache
            case _: raise ValueError( f"Invalid cache type: { cache }" )

    def _create_state (
        self,
        res: HttpResponse,
        prev: ResourceState | None = None
    ) -> ResourceState:
        """Create a cached resource state from an HTTP response."""

        created = time()

        max_age = next( (
            int( p.split( "=" )[ 1 ] )
            for p in res.headers.get( "Cache-Control", "" ).split( "," )
            if p.strip().startswith( "max-age=" )
        ), None )

        expires = created + max_age if max_age is not None else getattr( prev, "expires", None )
        etag = res.headers.get( "ETag" ) or getattr( prev, "etag", None )
        last_modified = res.headers.get( "Last-Modified" ) or getattr( prev, "last_modified", None )

        if res.status == 304 and prev:
            res = HttpResponse(
                prev.response.url, prev.response.ok, prev.response.status,
                prev.response.body, res.headers, res.latency
            )

        return ResourceState( res, created, expires, etag, last_modified )

    async def _fetch (
        self, path: str, *,
        prev: ResourceState | None = None,
        headers: HttpHeader = None,
        mode: RateLimitMode = "burst",
        timeout: float | None = None
    ) -> ResourceState:
        """Fetch a resource from the network."""

        headers = httpx.Headers( headers or {} )

        if prev and prev.etag:
            headers[ "If-None-Match" ] = prev.etag
        if prev and prev.last_modified:
            headers[ "If-Modified-Since" ] = prev.last_modified

        res = await self._client.request( path, headers= headers, mode= mode, timeout= timeout )
        return self._create_state( res, prev )

    async def refresh (
        self, path: str, *,
        headers: HttpHeader = None,
        mode: RateLimitMode = "burst",
        timeout: float | None = None
    ) -> ResourceState:
        """Refresh a cached resource."""

        state = await self._fetch(
            path, prev= await self._cache.get( path ),
            headers= headers, mode= mode, timeout= timeout
        )

        await self._cache.set( path, state )
        return state
