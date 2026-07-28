"""
HTTP Client

Implements an HTTP client with built-in rate limiting, request deduplication
and client identification.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from time import perf_counter
from typing import Literal
from urllib.parse import urljoin

import httpx
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
