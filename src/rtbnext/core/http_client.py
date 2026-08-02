"""
HTTP Client

Implements an HTTP client with built-in rate limiting, request deduplication
and proper client identification.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from time import perf_counter
from urllib.parse import urljoin

import httpx

from rtbnext._version import __version__
from rtbnext.core.rate_limiter import RateLimiter, RateLimitMode
from rtbnext.defaults import (
    DEFAULT_API_URL, DEFAULT_MAX_REQUESTS, DEFAULT_PER_SECONDS, DEFAULT_RATE_LIMIT_MODE,
    DEFAULT_TIMEOUT
)

type HttpHeader = httpx.Headers | dict[ str, str ] | None


@dataclass( slots= True, frozen= True )
class ClientIdentity:
    """Information used to identify the client making API requests."""

    name: str
    version: str
    contact: str | None = None
    email: str | None = None

    def __post_init__( self ) -> None:
        if not self.name.strip():
            raise ValueError( "Client name is required." )
        if not self.version.strip():
            raise ValueError( "Client version is required." )


@dataclass( slots= True, frozen= True, kw_only= True )
class HttpResponse:
    """Represents the response returned by an HTTP request."""

    url: str
    ok: bool
    status: int
    body: bytes
    headers: httpx.Headers
    latency: int


class HttpClient:
    """
    HTTP client with built-in rate limiting and request deduplication.

    Concurrent requests to the same URL share the same underlying request,
    preventing duplicate network traffic.
    """

    def __init__(
        self, client: ClientIdentity, *,
        base_url: str = DEFAULT_API_URL,
        max_requests: int = DEFAULT_MAX_REQUESTS,
        per_seconds: float = DEFAULT_PER_SECONDS,
        timeout: float = DEFAULT_TIMEOUT
    ) -> None:
        self._base_url, self._client_info, self._timeout = base_url, client, timeout

        self._limiter = RateLimiter( max_requests, per_seconds )
        self._client = httpx.AsyncClient( headers= self._create_headers(), follow_redirects= True )
        self._pending: dict[ str, asyncio.Task[ HttpResponse ] ] = {}

    async def __aenter__( self ) -> HttpClient:
        return self

    async def __aexit__( self, *_ ) -> None:
        await self.aclose()

    def _create_headers( self ) -> httpx.Headers:
        """Creates the default headers sent with every request."""

        client = self._client_info
        info = "; ".join( value for value in ( client.contact, client.email ) if value )

        headers = httpx.Headers( {
            "User-Agent": (
                f"{ client.name }/{ client.version }"
                f"{ f' ({ info })' if info else '' }"
                f" @rtbnext/sdk/{ __version__ }"
            ),
            "X-Client-Name": client.name,
            "X-Client-Version": client.version
        } )

        if client.contact:
            headers[ "X-Client-Contact" ] = client.contact

        return headers

    async def _execute(
        self, url: str, *,
        headers: HttpHeader = None,
        mode: RateLimitMode = DEFAULT_RATE_LIMIT_MODE,
        timeout: float | None = None
    ) -> HttpResponse:
        """Executes a single HTTP request."""

        await self._limiter.acquire( mode )

        try:
            start = perf_counter()
            res = await self._client.get(
                url, headers= headers, timeout= self._timeout if timeout is None else timeout
            )

        except httpx.HTTPError as exc:
            raise RuntimeError( f"Fetch failed: { exc }" ) from exc

        return HttpResponse(
            url= str( res.url ), ok= res.is_success, status= res.status_code, body= res.content,
            headers= res.headers, latency= round( ( perf_counter() - start ) * 1000 )
        )

    async def request(
        self, path: str, *,
        headers: HttpHeader = None,
        mode: RateLimitMode = DEFAULT_RATE_LIMIT_MODE,
        timeout: float | None = None
    ) -> HttpResponse:
        """Sends a request relative to the configured base URL."""

        url = urljoin( self._base_url, path )

        if task := self._pending.get( url ):
            return await task

        self._pending[ url ] = task = asyncio.create_task( self._execute(
            url, headers= headers, mode= mode, timeout= timeout
        ) )

        try:
            return await task
        finally:
            self._pending.pop( url, None )

    async def aclose( self ) -> None:
        """Closes the underlying HTTP client and release network resources."""

        await self._client.aclose()
