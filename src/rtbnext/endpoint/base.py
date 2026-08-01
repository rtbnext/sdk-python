"""
Base Endpoint

Implements the base endpoint class.
"""

from __future__ import annotations

from typing import Any

from rtbnext.core.loader import ResourceStateLoader
from rtbnext.resource.base import ResourcePool


class EndpointBase:
    """
    Base class for all API endpoints.

    Provides shared resource factory helpers for basic, collectable,
    indexable, time series, and dateable resources.
    """

    def __init__( self, loader: ResourceStateLoader, pool: ResourcePool, endpoints: Any ) -> None:
        self._loader, self._pool, self._endpoints = loader, pool, endpoints
