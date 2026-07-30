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
from rtbnext.resource.time_series import PointFn, TimeSeriesResource, TimeSeriesRow


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

        ...

    def csv(
        self, path: str, *,
        point: PointFn | None = None
    ) -> Resource:
        """Creates a CSV resource."""

        ...
