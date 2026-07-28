"""
Cache

Implements a cache interface for storing and retrieving resource states.

The cache protocol can be used to implement different storage backends,
such as in-memory caches or external databases.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from rtbnext.core.http_client import HttpResponse


@dataclass( slots= True )
class ResourceState:
    """Represents the state of a cached resource."""

    response: HttpResponse
    created: float
    expires: float | None = None
    etag: str | None = None
    last_modified: str | None = None


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
