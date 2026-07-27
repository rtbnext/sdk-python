"""
CACHE

Implements a cache interface for storing and retrieving resource states.
"""


from __future__ import annotations

from typing import Protocol

from rtbnext.core.resource import ResourceState


class Cache ( Protocol ):
    """
    Interface for cache implementations.

    A cache stores and retrieves resource states using string keys.
    Implementations may choose any storage backend, such as memory,
    the filesystem or an external database.
    """

    @property
    def size ( self ) -> int:
        """
        Return the number of cached resource states.
        """
        ...

    async def get ( self, key: str ) -> ResourceState | None:
        """
        Retrieve a cached resource state.

        Args:
            key:
                The cache key associated with the resource.

        Returns:
            The cached resource state if present, otherwise ``None``.
        """
        ...

    async def set ( self, key: str, value: ResourceState ) -> None:
        """
        Store a resource state.

        If the key already exists, the previous value is replaced.

        Args:
            key:
                The cache key.

            value:
                The resource state to store.
        """
        ...

    async def delete ( self, key: str ) -> None:
        """
        Remove a resource state from the cache.

        Args:
            key:
                The cache key.
        """
        ...

    async def clear ( self ) -> None:
        """
        Remove all resource states from the cache.
        """
        ...


class EmptyCache ( Cache ):
    """
    Cache implementation that never stores any data.

    All read operations return ``None``, while write operations are ignored.
    This implementation can be used to disable caching without changing the
    SDK's cache interface.
    """

    @property
    def size ( self ) -> int:
        return 0

    async def get ( self, _key: str ) -> ResourceState | None:
        return None

    async def set ( self, _key: str, _value: ResourceState ) -> None:
        return

    async def delete ( self, _key: str ) -> None:
        return

    async def clear ( self ) -> None:
        return


class MemoryCache ( Cache ):
    """
    Simple in-memory cache backed by a dictionary.

    Suitable for short-lived applications where persistence is not required.
    Cached entries remain until they are explicitly removed or the cache is
    cleared.
    """

    def __init__ ( self ) -> None:
        """
        Create an empty in-memory cache.
        """

        self._store: dict[ str, ResourceState ] = {}

    @property
    def size ( self ) -> int:
        return len( self._store )

    async def get ( self, key: str ) -> ResourceState | None:
        return self._store.get( key )

    async def set ( self, key: str, value: ResourceState ) -> None:
        self._store[ key ] = value

    async def delete ( self, key: str ) -> None:
        self._store.pop( key, None )

    async def clear ( self ) -> None:
        self._store.clear()
