from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from urllib.parse import urljoin
import asyncio
import httpx

from .rate_limiter import RateLimiter, RateLimiterOptions


@dataclass ( slots= True, frozen= True )
class ClientIdentity:
  """
  Information used to identify the client making API requests.
  """

  name: str
  version: str | int
  contact: str | None = None
  email: str | None = None


@dataclass ( slots= True, frozen= True )
class HttpClientOptions:
  """
  Configuration options for the HTTP client.
  """

  base_url: str
  sdk_version: str
  client: ClientIdentity
  limiter: RateLimiterOptions
  timeout: float
