"""
Base Resource

Implements the base resource wrapper for HTTP responses.
Resource instance pooling is intended to optimize memory allocation.
"""

from __future__ import annotations

import asyncio
from typing import Any, Awaitable, Callable, Generic, Self, TypeVar

from rtbnext.core.loader import ResourceLoader, ResourceState
from rtbnext.core.parser import ParserFn

D = TypeVar( "D" )
R = TypeVar( "R", bound= "Resource[ Any ]" )


class Resource( Generic[ D ] ):
    """
    Base resource wrapper for lazy loading, parsing and cache state management.

    Resources are loaded only when data is requested. Loaded responses are kept
    as resource state while parsed values are cached separately.
    """

    def __init__( self, path: str, loader: ResourceLoader, parser: ParserFn[ D ] ) -> None:
        self._path, self._loader, self._parser = path, loader, parser

        self._hooks: dict[ str, set[ Callable[ [ Self ], None ] ] ] = {}

        self._state: ResourceState | None = None
        self._loading: asyncio.Task[ None ] | None = None
        self._loaded = False

        self._parsed = False
        self._value: D | None = None

        self._transformed: Any | Awaitable[ Any ] | None = None


class ResourcePool( Generic[ R ] ):
    """
    Stores and reuses resource instances by their resource path.

    Valid resources are reused, while invalid resources are replaced with
    newly created instances.
    """

    def __init__( self ) -> None:
        self._resources: dict[ str, R ] = {}

    def get( self, path: str, factory: Callable[ [], R ] ) -> R:
        """Return an existing valid resource or create a new one."""

        if ( res := self._resources.get( path ) ) and getattr( res, "valid", False ):
            return res

        self._resources[ path ] = res = factory()
        return res

    @property
    def size( self ) -> int:
        """Return the number of pooled resources."""

        return len( self._resources )

    def delete( self, path: str ) -> None:
        """Delete a resource from the cache by path."""

        self._resources.pop( path, None )

    def clear( self ) -> None:
        """Remove all pooled resources."""

        self._resources.clear()
