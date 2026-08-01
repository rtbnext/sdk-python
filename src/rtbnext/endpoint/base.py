"""
Base Endpoint

Implements the base endpoint class.
"""

from __future__ import annotations

from typing import Any

from rtbnext.core.loader import ResourceStateLoader
from rtbnext.resource.base import Resource, ResourcePool
from rtbnext.resource.collectable import CollectableResource
from rtbnext.resource.indexable import IndexableResource


class EndpointBase:
    """
    Base class for all API endpoints.

    Provides shared resource factory helpers for basic, collectable,
    indexable, time series, and dateable resources.
    """

    def __init__( self, loader: ResourceStateLoader, pool: ResourcePool, endpoints: Any ) -> None:
        self._loader, self._pool, self._endpoints = loader, pool, endpoints

    def _resource( self ) -> Resource:
        ...

    def _collectable( self ) -> CollectableResource:
        ...

    def _dateable( self ) -> Resource:
        ...

    def _indexable( self ) -> IndexableResource:
        ...

    def _series( self ) -> Resource:
        ...
