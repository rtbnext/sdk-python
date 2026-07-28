"""
Resource

Implements the resource loader and pooling of resource states.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypeAlias

from rtbnext.core.cache import Cache, EmptyCache, MemoryCache
from rtbnext.core.http_client import HttpClient, HttpResponse

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
