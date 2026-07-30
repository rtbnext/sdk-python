"""
HTTP Client

Implements an HTTP client with built-in rate limiting, request deduplication
and proper client identification.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass

import httpx

from rtbnext.core.rate_limiter import RateLimiter, RateLimitMode
from rtbnext.defaults import (
    DEFAULT_API_URL, DEFAULT_MAX_REQUESTS, DEFAULT_PER_SECONDS, DEFAULT_RATE_LIMIT_MODE,
    DEFAULT_TIMEOUT
)


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
