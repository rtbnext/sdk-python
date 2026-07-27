from __future__ import annotations

import asyncio
from dataclasses import dataclass
from time import perf_counter
from typing import Literal
from urllib.parse import urljoin

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


@dataclass ( slots= True, frozen= True )
class RequestOptions:
  """
  Options for an individual HTTP request.
  """

  headers: dict[ str, str ] | None = None
  mode: Literal[ "burst", "spread" ] = "burst"
  timeout: float | None = None


@dataclass ( slots= True, frozen= True )
class HttpResponse:
  """
  Represents the response returned by an HTTP request.
  """

  url: str
  ok: bool
  status: int
  body: bytes
  headers: httpx.Headers
  latency: int
