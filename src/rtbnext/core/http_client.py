"""
HTTP Client

Implements an HTTP client with built-in rate limiting, request deduplication
and proper client identification.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from time import perf_counter
from typing import Literal
from urllib.parse import urljoin

import httpx
from rtbnext import __api__, __version__
from rtbnext.core.rate_limiter import RateLimiter


@dataclass( slots= True, frozen= True )
class ClientIdentity:
    """Information used to identify the client making API requests."""

    name: str
    version: str
    contact: str | None = None
    email: str | None = None


@dataclass( slots= True, frozen= True )
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
        self,
        *,
        client: ClientIdentity,
        base_url: str = __api__,
        max_requests: int = 60,
        per_seconds: int = 10,
        timeout: float = 30
    ) -> None:
        self._base_url = base_url
        self._client_info = client
        self._timeout = timeout

        self._limiter = RateLimiter( max_requests, per_seconds )
        self._pending: dict[ str, asyncio.Task[ HttpResponse ] ] = {}

        self._client = httpx.AsyncClient(
            headers= self._create_headers(),
            follow_redirects= True
        )

    def _create_headers( self ) -> httpx.Headers:
        """Create the default headers sent with every request."""

        client = self._client_info

        if not client.name.strip():
            raise ValueError( "Client name is required." )
        if not client.version.strip():
            raise ValueError( "Client version is required." )

        info = "; ".join( value for value in ( client.contact, client.email ) if value )

        headers = httpx.Headers( {
            "User-Agent": (
                f"{ client.name }/{ client.version }"
                f"{ f' ({ info })' if info else '' }"
                f" @rtbnext/sdk/{ __version__ }"
            ),
            "X-Client-Name": client.name,
            "X-Client-Version": client.version,
        } )

        if client.contact:
            headers[ "X-Client-Contact" ] = client.contact

        return headers
