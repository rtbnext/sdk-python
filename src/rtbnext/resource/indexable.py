"""
Indexable Resource

Implement the resource wrapper for nested indexable endpoints.
"""


from __future__ import annotations

from typing import Callable, Generic, TypeVar

from rtbnext.core.parser import D, ParserFn
from rtbnext.core.resource import ResourceLoader
from rtbnext.resource.base import Resource

R = TypeVar( "R" )
type PathParts = tuple[ str, ... ]
type IndexFn[ R ] = Callable[ [ tuple[ str, ... ] ], R ]
type KeysFn = Callable[ [ object ], tuple[ str, ... ] | None ]


class _IndexAccessor( Generic[ R ] ):
    """Lazy accessor object for index traversal."""

    def __init__( self, factory: IndexFn[ R ], path: PathParts, keys: PathParts ) -> None:
        self._factory, self._path, self._keys = factory, path, keys

    def __getattr__( self, key: str ) -> R:
        """Resolve a nested resource."""

        if key not in self._keys:
            raise AttributeError( f"Unknown index key: { key }" )

        return self._factory( ( *self._path, key ) )
