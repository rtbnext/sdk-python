"""
Base Endpoint

Implements the base endpoint class.
"""

from __future__ import annotations

from typing import Any

from rtbnext.core.parser import Parser, ParserFn
from rtbnext.core.resource import ResourceLoader, ResourcePool
from rtbnext.resource.base import Resource
from rtbnext.resource.collectable import CollectableResource
from rtbnext.resource.dateable import DateableResource
from rtbnext.resource.indexable import IndexableResource
from rtbnext.resource.time_series import TimeSeriesResource


class EndpointBase:
    """
    Base class for all API endpoints.

    Provides shared resource factory helpers for text, JSON, CSV,
    collection, index, time series, and date resources.
    """

    def _resource(
        self,
        path: str,
        parser: ParserFn,
        resources: list[ tuple[ str, type[ Resource ] ] ],
        **options: Any
    ) -> Resource:
        """Resolve the resource by its factory method."""

        args = ( path, self._loader, parser )

        if not options:
            return self._pool.get( path, lambda: Resource( *args ) )

        for key, cls in resources:
            if key in options:
                return self._pool.get( path, lambda: cls( *args, **options ) )

        raise ValueError( "Invalid resource options" )

    def __init__( self, loader: ResourceLoader, pool: ResourcePool, endpoints: Any ) -> None:
        self._loader, self._pool, self._endpoints = loader, pool, endpoints

    def text( self, path: str ) -> Resource:
        """Creates a text resource."""

        return self._pool.get( path, lambda: Resource( path, self._loader, Parser.text ) )

    def json( self, path: str, **options: Any ) -> Resource:
        """Creates a JSON resource."""

        return self._resource( path, Parser.json, [
            ( "entity", CollectableResource ),
            ( "date_factory", DateableResource ),
            ( "index", IndexableResource )
        ], **options )

    def csv( self, path: str, **options: Any ) -> Resource:
        """Creates a CSV resource."""

        return self._resource( path, Parser.csv, [
            ( "point", TimeSeriesResource )
        ], **options )
