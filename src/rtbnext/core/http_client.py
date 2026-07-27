from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from urllib.parse import urljoin
import asyncio
import httpx

from .rate_limiter import RateLimiter, RateLimiterOptions
