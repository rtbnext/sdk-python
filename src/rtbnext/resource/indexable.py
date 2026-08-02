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
type KeysFn = Callable[ [ object ], list[ str ] | None ]


class _IndexAccessor( Generic[ R ] ):
    """Lazy accessor object for index traversal."""

    def __init__( self, factory: IndexFn[ R ], keys: KeysFn, path: Path, value: object ) -> None:
        self._factory, self._keys, self._path, self._value = factory, keys, path, value

    def __getitem__( self, key: str ) -> R | _IndexAccessor[ R ]:
        """Resolves a nested index key."""

        available = self._keys( self._value )

        if available is None or key not in available:
            raise AttributeError( f"Unknown index key: { key }" )

        path = ( *self._path, key )

        if isinstance( self._value, dict ):
            child = self._value[ key ]

            if isinstance( child, ( dict, list ) ):
                return _IndexAccessor( self._factory, self._keys, path, child )

        return self._factory( path )

    def __dir__( self ) -> list[ str ]:
        """Returns available index keys."""

        return sorted( [ *super().__dir__(), *( self._keys( self._value ) or [] ) ] )


class IndexableResource( Resource[ D ], Generic[ D, R ] ):
    """
    Resource wrapper for nested indexable endpoints.

    This class provides lazy traversal over API indexes by exposing generated
    accessors for nested keys.

    The underlying resource data is loaded only once and transformed into a
    reusable accessor tree.
    """

    def __init__(
        self, path: str, loader: ResourceStateLoader, parser: ParserFn[ D ], *,
        index: IndexFn[ R ],
        keys: KeysFn | None = None
    ) -> None:
        super().__init__( path, loader, parser )

        self._factory = index
        self._keys = keys or self._default_keys

    @staticmethod
    def _default_keys( value: object ) -> list[ str ] | None:
        """Extracts keys from common index structures."""

        if isinstance( value, dict ):
            return list( value.keys() )

        if isinstance( value, list ):
            return [ str( item ) for item in value ]

        return None

    def _traverse( self, value: object, path: Path = () ) -> _IndexAccessor[ R ]:
        """Creates the lazy accessor tree."""

        return _IndexAccessor( self._factory, self._keys, path, value )

    async def get( self ) -> R:
        """Returns the lazily generated index tree."""

        return await self._transform( self._traverse )
