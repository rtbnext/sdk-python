"""
RESOURCE

Implements the resource loader and pooling of resource states.
"""


from __future__ import annotations
from dataclasses import dataclass
from time import time
from typing import Any, Callable, Generic, Literal, TypeVar, TYPE_CHECKING
import httpx
from rtbnext.core.http_client import HttpResponse, HttpClient, RequestOptions
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

    def _create_state (
        self,
        response: HttpResponse,
        previous: ResourceState | None = None
    ) -> ResourceState:
        """
        Create a cached resource state from an HTTP response.

        Args:
            response:
                HTTP response returned by the server.

            previous:
                Previous cached resource state.

        Returns:
            The updated resource state.
        """

        now = time()
        cache_control = response.headers.get( "Cache-Control", "" )

        max_age = next(
            (
                int( part.split( "=" )[ 1 ] )
                for part in cache_control.split( "," )
                if part.strip().startswith( "max-age=" )
            ),
            None
        )

        expires = (
            now + max_age
            if max_age is not None
            else previous.expires if previous else None
        )

        etag = response.headers.get( "ETag" ) or (
            previous.etag if previous else None
        )

        last_modified = response.headers.get( "Last-Modified" ) or (
            previous.last_modified if previous else None
        )

        if response.status == 304 and previous:
            response = type( response )(
                url= response.url,
                ok= True,
                status= previous.response.status,
                body= previous.response.body,
                headers= response.headers,
                latency= response.latency
            )

        return ResourceState(
            response= response,
            created= now,
            expires= expires,
            etag= etag,
            last_modified= last_modified
        )

    async def _fetch (
        self,
        path: str,
        previous: ResourceState | None = None,
        options: RequestOptions | None = None
    ) -> ResourceState:
        """
        Fetch a resource from the network.

        Conditional request headers are automatically added when a previous
        resource state is available.

        Args:
            path:
                Resource path.

            previous:
                Previous cached resource state.

            options:
                Additional request options.

        Returns:
            The updated resource state.
        """

        headers = httpx.Headers( options.headers if options else None )

        if previous and previous.etag:
            headers[ "If-None-Match" ] = previous.etag
        if previous and previous.last_modified:
            headers[ "If-Modified-Since" ] = previous.last_modified

        request_options = RequestOptions(
            headers= headers,
            mode= options.mode if options else "burst",
            timeout= options.timeout if options else None
        )

        response = await self._client.request( path, request_options )
        return self._create_state( response, previous )
