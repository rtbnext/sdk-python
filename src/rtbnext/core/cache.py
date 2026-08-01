"""
Cache

Implements a cache interface for storing and retrieving resource states.

The cache protocol can be used to implement different storage backends,
such as in-memory caches or external databases.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from rtbnext.core.resource import ResourceState


@runtime_checkable
class Cache( Protocol ):
    """
    Interface for cache implementations.

    A cache stores and retrieves resource states using string keys.
    Implementations may choose any storage backend, such as memory,
    the filesystem or an external database.
    """

    @property
    def size( self ) -> int:
        """Return the number of cached resource states."""
        ...

    async def get( self, key: str ) -> ResourceState | None:
        """Retrieve a cached resource state."""
        ...

    async def set( self, key: str, value: ResourceState ) -> None:
        """Store a resource state."""
        ...

    async def delete( self, key: str ) -> None:
        """Remove a resource state from the cache."""
        ...

    async def clear( self ) -> None:
        """Remove all resource states from the cache."""
        ...
