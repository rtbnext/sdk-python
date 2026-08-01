"""
Resource

Implements the resource loader and pooling of resource states.
"""

from __future__ import annotations

from dataclasses import dataclass
from time import time
from typing import TYPE_CHECKING, Callable, Generic, Literal, TypeVar

import httpx

from rtbnext.core.http_client import HttpResponse
from rtbnext.defaults import DEFAULT_RATE_LIMIT_MODE, DEFAULT_TIMEOUT

if TYPE_CHECKING:
    from typing import Any

    from rtbnext.core.http_client import HttpClient, HttpHeader, RateLimitMode
