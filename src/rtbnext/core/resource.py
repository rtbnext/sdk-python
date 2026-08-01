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
from rtbnext.defaults import (
    DEFAULT_CACHE_MODE, DEFAULT_CACHE_TYPE, DEFAULT_RATE_LIMIT_MODE, DEFAULT_TIMEOUT
)

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
