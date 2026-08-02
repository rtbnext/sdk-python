"""
Base Endpoint

Implements the base endpoint class.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rtbnext.core.loader import ResourceStateLoader
from rtbnext.core.parser import Parser, ParserMode, parser
from rtbnext.resource.base import Resource, ResourcePool
from rtbnext.resource.collectable import CollectableResource, EntityFn, FindFn, SearchFn
from rtbnext.resource.dateable import DateableResource, DateFn
from rtbnext.resource.indexable import IndexableResource, IndexFn, KeysFn

if TYPE_CHECKING:
    from rtbnext.rtbnext import Endpoints


class EndpointBase:
    """
    Base class for all API endpoints.

    Provides shared resource factory helpers for basic, collectable,
    indexable, time series, and dateable resources.
    """

    def __init__(
        self,
        loader: ResourceStateLoader,
        pool: ResourcePool,
        endpoints: Endpoints
    ) -> None:
        self._loader, self._pool, self._endpoints = loader, pool, endpoints

    def _resource( self, path: str, mode: ParserMode = "json" ) -> Resource:
        """Returns a basic resource."""

        return self._pool.get( path, lambda: Resource( path, self._loader, parser( mode ) ) )

    def _collectable(
        self, path: str, *,
        entity: EntityFn,
        find: FindFn | None = None,
        search: SearchFn | None = None
    ) -> CollectableResource:
        """Returns a collectable resource."""

        return self._pool.get( path, lambda: CollectableResource(
            path, self._loader, Parser.json, entity= entity, find= find, search= search
        ) )

    def _dateable( self, path: str, *, date: DateFn ) -> DateableResource:
        """Returns a dateable resource."""

        return self._pool.get( path, lambda: DateableResource(
            path, self._loader, Parser.json, date= date
        ) )

    def _indexable(
        self, path: str, *,
        index: IndexFn,
        keys: KeysFn | None = None
    ) -> IndexableResource:
        """Returns a indexable resource."""

        return self._pool.get( path, lambda: IndexableResource(
            path, self._loader, Parser.json, index= index, keys= keys
        ) )

    def _series( self ) -> Resource:
        """Returns a time series resource."""
        ...
