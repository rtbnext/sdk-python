"""
Resource

Implements the resource loader and pooling of resource states.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Any, Callable, Generic, Literal, TypeVar

import httpx

from rtbnext.core.cache import Cache, EmptyCache, MemoryCache
from rtbnext.core.http_client import HttpClient, HttpHeader, HttpResponse, RateLimitMode
from rtbnext.defaults import DEFAULT_CACHE_MODE, DEFAULT_CACHE_TYPE, DEFAULT_RATE_LIMIT_MODE

type CacheType = Cache | Literal[ "memory", False ]
type CacheMode = Literal[ "ttl", "session", "revalidate" ]


@dataclass( slots= True, kw_only= True )
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
        cache: CacheType = DEFAULT_CACHE_TYPE,
        mode: CacheMode = DEFAULT_CACHE_MODE
    ) -> None:
        self._client, self._mode = client, mode

        match cache:
            case "memory": self._cache = MemoryCache()
            case False: self._cache = EmptyCache()
            case _ if isinstance( cache, Cache ): self._cache = cache
            case _: raise ValueError( f"Invalid cache type: { cache }" )

    def _state( self, res: HttpResponse, prev: ResourceState | None = None ) -> ResourceState:
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
                url= prev.response.url, ok= prev.response.ok, status= prev.response.status,
                body= prev.response.body, headers= res.headers, latency= res.latency
            )

        return ResourceState(
            response= res, created= created, expires= expires,
            etag= etag, last_modified= last_modified
        )

    async def _fetch(
        self, path: str, prev: ResourceState | None = None, *,
        headers: HttpHeader = None,
        mode: RateLimitMode = DEFAULT_RATE_LIMIT_MODE,
        timeout: float | None = None
    ) -> ResourceState:
        """Fetch a resource from the network."""

        headers = httpx.Headers( headers or {} )

        if prev and prev.etag:
            headers[ "If-None-Match" ] = prev.etag
        if prev and prev.last_modified:
            headers[ "If-Modified-Since" ] = prev.last_modified

        res = await self._client.request( path, headers= headers, mode= mode, timeout= timeout )
        return self._state( res, prev )
