"""
Indexable Resource

Implement the resource wrapper for nested indexable endpoints.
"""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

from rtbnext.core.loader import ResourceStateLoader
from rtbnext.core.parser import ParserFn
from rtbnext.resource.base import Resource

D = TypeVar( "D" )
R = TypeVar( "R" )

type Path = tuple[ str, ... ]
type IndexFn[ R ] = Callable[ [ Path ], R ]
type KeysFn = Callable[ [ object ], Path | None ]


class _IndexAccessor( Generic[ R ] ):
    """Lazy accessor object for index traversal."""

    def __init__( self, factory: IndexFn[ R ], path: Path, keys: Path ) -> None:
        self._factory, self._path, self._keys = factory, path, keys

    def __getattr__( self, key: str ) -> R:
        """Resolve a nested resource."""

        if key not in self._keys:
            raise AttributeError( f"Unknown index key: { key }" )

        return self._factory( ( *self._path, key ) )

    def __dir__( self ) -> list[ str ]:
        """Return the list of available index keys."""

        return sorted( ( *super().__dir__(), *self._keys ) )
