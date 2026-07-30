"""
Base Endpoint

Implements the base endpoint class.
"""

from __future__ import annotations

from typing import Any

from rtbnext.core.parser import Parser
from rtbnext.core.resource import ResourceLoader, ResourcePool
from rtbnext.resource.base import Resource
from rtbnext.resource.collectable import CollectableResource
from rtbnext.resource.dateable import DateableResource
from rtbnext.resource.time_series import TimeSeriesResource


class EndpointBase:
    """
    Base class for all API endpoints.

    Provides shared resource factory helpers for text, JSON, CSV,
    collection, index, time series, and date resources.
    """

    def __init__( self, loader: ResourceLoader, pool: ResourcePool, endpoints: Any ) -> None:
        self._loader, self._pool, self._endpoints = loader, pool, endpoints

    def text( self, path: str ) -> Resource:
        """Creates a text resource."""

        return self._pool.get( path, lambda: Resource( path, self._loader, Parser.text ) )

    def json( self, path: str, **options: Any ) -> Resource:
        """Creates a JSON resource."""

        def factory() -> Resource:
            args = ( path, self._loader, Parser.json )

            if not options:
                return Resource( *args )

        return self._pool.get( path, factory )
