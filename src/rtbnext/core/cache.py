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


class EmptyCache( Cache ):
    """
    Cache implementation that never stores any data.

    All read operations return `None`, while write operations are ignored.
    This implementation can be used to disable caching without changing the
    SDK's cache interface.
    """

    @property
    def size( self ) -> int:
        return 0

    async def get( self, _key: str ) -> ResourceState | None:
        return None

    async def set( self, _key: str, _value: ResourceState ) -> None:
        pass

    async def delete( self, _key: str ) -> None:
        pass

    async def clear( self ) -> None:
        pass


class MemoryCache ( Cache ):
    """
    Simple in-memory cache backed by a dictionary.

    Suitable for short-lived applications where persistence is not required.
    Cached entries remain until they are explicitly removed or the cache is
    cleared.
    """

    def __init__( self ) -> None:
        self._store: dict[ str, ResourceState ] = {}

    @property
    def size( self ) -> int:
        return len( self._store )

    async def get( self, key: str ) -> ResourceState | None:
        return self._store.get( key )

    async def set( self, key: str, value: ResourceState ) -> None:
        self._store[ key ] = value

    async def delete( self, key: str ) -> None:
        self._store.pop( key, None )

    async def clear( self ) -> None:
        self._store.clear()
