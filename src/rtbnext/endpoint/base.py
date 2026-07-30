"""
Base Endpoint

Implements the base endpoint class.
"""

from __future__ import annotations

from typing import Any

from rtbnext.core.parser import Parser, ParserFn
from rtbnext.core.resource import ResourceLoader, ResourcePool
from rtbnext.resource.base import Resource
from rtbnext.resource.collectable import CollectableResource, EntityFn, FindFn, SearchFn
from rtbnext.resource.dateable import DateableResource, DateFn
from rtbnext.resource.indexable import IndexableResource, IndexFn, KeysFn
from rtbnext.resource.time_series import PointFn, TimeSeriesResource


class EndpointBase:
    """
    Base class for all API endpoints.

    Provides shared resource factory helpers for text, JSON, CSV,
    collection, index, time series, and date resources.
    """

    def __init__( self, loader: ResourceLoader, pool: ResourcePool, endpoints: Any ) -> None:
        self._loader, self._pool, self._endpoints = loader, pool, endpoints

    def _resource(
        self,
        path: str,
        parser: ParserFn,
        resources: list[ tuple[ str, type[ Resource ], dict[ str, Any ] ] ]
    ) -> Resource:
        """Resolve the resource by its factory method."""

        args = ( path, self._loader, parser )

        for key, cls, options in resources:
            if options[ key ] is not None:
                return self._pool.get( path, lambda: cls( *args, **{
                    k: v for k, v in options.items()
                    if v is not None
                } ) )

        return self._pool.get( path, lambda: Resource( *args ) )

    def text( self, path: str ) -> Resource:
        """Creates a text resource."""

        return self._pool.get( path, lambda: Resource( path, self._loader, Parser.text ) )

    def json(
        self, path: str, *,
        entity: EntityFn | None = None,
        find: FindFn | None = None,
        search: SearchFn | None = None,
        date: DateFn | None = None,
        index: IndexFn | None = None,
        keys: KeysFn | None = None
    ) -> Resource:
        """Creates a JSON resource."""

        return self._resource( path, Parser.json, [
            ( "entity", CollectableResource, { "entity": entity, "find": find, "search": search } ),
            ( "date", DateableResource, { "date_factory": date } ),
            ( "index", IndexableResource, { "index": index, "keys": keys } )
        ] )

    def csv(
        self, path: str, *,
        point: PointFn | None = None
    ) -> Resource:
        """Creates a CSV resource."""

        return self._resource( path, Parser.csv, [
            ( "point", TimeSeriesResource, { "point": point }
        ) ] )
