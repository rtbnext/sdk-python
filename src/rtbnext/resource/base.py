"""
Base Resource

Implements the base resource wrapper for HTTP responses.
Resource instance pooling is intended to optimize memory allocation.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar, Callable

D = TypeVar( "D" )
R = TypeVar( "R", bound= "Resource[ Any ]" )


class Resource( Generic[ D ] ):
    ...


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
