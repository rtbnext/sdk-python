"""
RESOURCE

Implements the resource loader and pooling of resource states.
"""


from __future__ import annotations
from dataclasses import dataclass
from time import time
from typing import Any, Callable, Generic, Literal, TypeVar, TYPE_CHECKING
import httpx
from rtbnext.core.http_client import HttpResponse, HttpClient
from rtbnext.core.cache import Cache, EmptyCache, MemoryCache
from rtbnext.resource.resource import Resource


CacheMode = Literal[ "ttl", "session", "revalidate" ]


@dataclass ( slots= True )
class CacheOptions:
    """
    Configuration options for the resource loader cache.
    """

    type: Cache | Literal[ False, "memory" ] = "memory"
    mode: CacheMode = "ttl"


@dataclass ( slots= True )
class ResourceState:
    """
    Represents the state of a cached resource.
    """

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

    def __init__ ( self, client: HttpClient, options: CacheOptions | None = None ) -> None:
        """
        Create a new resource loader.

        Args:
            client:
                HTTP client used to perform resource requests.

            options:
                Cache configuration.
        """

        options = options or CacheOptions()

        self._client = client
        self._mode = options.mode

        match options.type:
            case False:
                self._cache = EmptyCache()
            case "memory":
                self._cache = MemoryCache()
            case _:
                self._cache = options.type
