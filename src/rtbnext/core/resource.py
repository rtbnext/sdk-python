"""
Resource

Implements the resource loader and pooling of resource states.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import Any, Callable, Generic, Literal, TypeVar

import httpx

from rtbnext.core.http_client import HttpResponse
from rtbnext.defaults import DEFAULT_RATE_LIMIT_MODE, DEFAULT_TIMEOUT
from rtbnext.core.http_client import HttpClient, HttpHeader, RateLimitMode

type CacheType = Literal[ False, "memory" ]
type CacheMode = Literal[ "ttl", "session", "revalidate" ]


@dataclass( slots= True, kw_only= True )
class ResourceState:
    """Represents the state of a cached resource."""

    response: HttpResponse
    created: float
    expires: float | None = None
    etag: str | None = None
    last_modified: str | None = None
