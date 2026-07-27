"""
HTTP CLIENT

Implements an HTTP client with built-in rate limiting and request deduplication.
"""


from __future__ import annotations

import asyncio
from dataclasses import dataclass
from time import perf_counter
from typing import Literal
from urllib.parse import urljoin

import httpx

from rtbnext.core.rate_limiter import RateLimiter, RateLimiterOptions


@dataclass ( slots= True, frozen= True )
class ClientIdentity:
    """Information used to identify the client making API requests."""

    name: str
    version: str | int
    contact: str | None = None
    email: str | None = None


@dataclass ( slots= True, frozen= True )
class HttpClientOptions:
    """Configuration options for the HTTP client."""

    base_url: str
    sdk_version: str
    client: ClientIdentity
    limiter: RateLimiterOptions
    timeout: float


@dataclass ( slots= True, frozen= True )
class RequestOptions:
    """Options for an individual HTTP request."""

    headers: httpx.Headers | dict[ str, str ] | None = None
    mode: Literal[ "burst", "spread" ] = "burst"
    timeout: float | None = None


@dataclass ( slots= True, frozen= True )
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

    def __init__ ( self, options: HttpClientOptions ) -> None:
        """
        Create a new HTTP client.

        Args:
            options:
                Configuration options for the client.
        """

        self._options = options
        self._limiter = RateLimiter( options.limiter )

        self._client = httpx.AsyncClient(
            headers= self._create_headers(),
            follow_redirects= True
        )

        self._pending: dict[ str, asyncio.Task[ HttpResponse ] ] = {}

    def _create_headers ( self ) -> httpx.Headers:
        """
        Create the default headers sent with every request.

        Returns:
            A configured set of HTTP headers.

        Raises:
            ValueError:
                If the client name or version is empty.
        """

        client = self._options.client

        if not client.name.strip():
            raise ValueError( "Client name is required." )
        if not str( client.version ).strip():
            raise ValueError("Client version is required.")

        info = "; ".join(
            value
            for value in ( client.contact, client.email )
            if value
        )

        agent = (
            f"{ client.name }/{ client.version }"
            f"{ f' ({ info })' if info else '' }"
            f" @rtbnext/sdk/{ self._options.sdk_version }"
        )

        headers: dict[ str, str ] = {
            "User-Agent": agent,
            "X-Client-Name": client.name,
            "X-Client-Version": str( client.version )
        }

        if client.contact:
            headers[ "X-Client-Contact" ] = client.contact

        return httpx.Headers( headers )

    async def _execute ( self, url: str, options: RequestOptions | None = None ) -> HttpResponse:
        """
        Execute a single HTTP request.

        Args:
            url:
                The absolute URL to request.

            options:
                Optional request-specific configuration.

        Returns:
            The HTTP response.

        Raises:
            RuntimeError:
                If the request could not be completed.
        """

        mode = options.mode if options else "burst"
        await getattr( self._limiter, mode )()

        try:
            start = perf_counter()

            response = await self._client.get(
                url,
                headers= options.headers if options else None,
                timeout= (
                    options.timeout
                    if options and options.timeout is not None
                    else self._options.timeout
                )
            )

            latency = round( ( perf_counter() - start ) * 1000 )

            return HttpResponse(
                url= str( response.url ),
                ok= response.is_success,
                status= response.status_code,
                body= response.content,
                headers= response.headers,
                latency= latency
            )

        except Exception as exc:
            raise RuntimeError( f"Fetch failed: { exc }" ) from exc

    async def request ( self, path: str, options: RequestOptions | None = None ) -> HttpResponse:
        """
        Send a request relative to the configured base URL.

        If another coroutine is already requesting the same URL,
        the existing request is reused.

        Args:
            path:
                Relative request path.
      
            options:
                Optional request configuration.
      
        Returns:
            The HTTP response.
        """

        url = urljoin( self._options.base_url, path )

        existing = self._pending.get( url )
        if existing:
            return await existing

        task = asyncio.create_task( self._execute( url, options ) )
        self._pending[ url ] = task

        try:
            return await task
        finally:
            self._pending.pop( url, None )

    async def aclose ( self ) -> None:
        """Close the underlying HTTP client and release network resources."""

        await self._client.aclose()

    async def __aenter__ ( self ) -> HttpClient:
        """Return the HTTP client when entering an async context."""

        return self

    async def __aexit__ ( self, *_ ):
        """Close the HTTP client when leaving an async context."""

        await self.aclose()
