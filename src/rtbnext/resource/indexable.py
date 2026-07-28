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


class IndexableResource( Resource[ D ], Generic[ D, R ] ):
    """
    Resource wrapper for nested indexable endpoints.

    This class provides lazy traversal over API indexes by exposing generated
    accessors for nested keys.

    The underlying resource data is loaded only once and transformed into a
    reusable accessor tree.
    """

    def __init__(
        self, path: str, *,
        loader: ResourceLoader,
        parser: ParserFn[ D ],
        index: IndexFn[ R ],
        keys: KeysFn | None
    ) -> None:
        super().__init__( path, loader= loader, parser= parser )

        self._factory = index
        self._keys = keys or self._default_keys

    @staticmethod
    def _default_keys( value: object ) -> PathParts | None:
        """Extract index keys from common API structures."""

        if isinstance( value, list ):
            return tuple( map( str, value ) )

        if isinstance( value, dict ) and isinstance( value.get( "items" ), dict ):
            return tuple( map( str, value[ "items" ] ) )

        return None

    def _create_index ( self, keys: PathParts, path: PathParts ) -> _IndexAccessor[ R ]:
        """Create a lazy accessor node."""

        return _IndexAccessor( self._factory, path, keys )

    def _traverse( self, value: object, path: PathParts = () ) -> object:
        """Convert parsed index data into an accessor tree."""

        if ( keys := self._keys( value ) ) is not None:
            return self._create_index( keys, path )

        if isinstance( value, dict ):
            return {
                key: self._traverse( val, ( *path, key ) )
                for key, val in value.items()
                if key != "$metadata"
            }

        return None

    async def get( self ) -> object:
        """Return the lazily generated index tree."""

        return await self._transform( self._traverse )
