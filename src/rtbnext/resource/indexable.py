"""Implement the resource wrapper for nested indexable endpoints."""


from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from rtbnext.core.parser import D, ParserFn
from rtbnext.core.resource import ResourceLoader
from rtbnext.resource.resource import Resource

R = TypeVar( "R" )
IndexFn = Callable[ [ tuple[ str, ... ] ], R ]
KeysFn = Callable[ [ object ], tuple[ str, ... ] | None ]


@dataclass ( slots= True )
class IndexOptions( Generic[ R ] ):
    """Configuration for index traversal."""

    index: IndexFn[ R ]
    keys: KeysFn | None = None


class _IndexAccessor ( Generic[ R ] ):
    """Lazy accessor object for index traversal."""

    def __init__ (
        self,
        factory: IndexFn[ R ],
        path: tuple[ str, ... ],
        keys: tuple[ str, ... ]
    ) -> None:
        self._factory = factory
        self._path = path
        self._keys = keys


    def __getattr__ ( self, key: str ) -> R:
        """Resolve a nested resource."""

        if key not in self._keys:
            raise AttributeError( f"Unknown index key: { key }" )
        return self._factory( ( *self._path, key ) )


class IndexableResource ( Resource[ D ], Generic[ D, R ] ):
    """
    Resource wrapper for nested indexable endpoints.

    This class provides lazy traversal over API indexes by exposing generated
    accessors for nested keys.

    The underlying resource data is loaded only once and transformed into a
    reusable accessor tree.
    """

    def __init__ (
        self,
        path: str,
        loader: ResourceLoader,
        parser: ParserFn[ D ],
        options: IndexOptions[ R ]
    ) -> None:
        super().__init__( path, loader, parser )

        self._factory = options.index
        self._keys = options.keys or self._default_keys

    @staticmethod
    def _default_keys ( value: object ) -> tuple[ str, ... ] | None:
        """Extract index keys from common API structures."""

        if isinstance( value, list ):
            return tuple( str( item ) for item in value )

        if isinstance( value, dict ):
            items = value.get( "items" )

            if isinstance( items, dict ):
                return tuple( str( key ) for key in items.keys() )

        return None

    def _create_index (
        self,
        keys: tuple[ str, ... ],
        path: tuple[ str, ... ]
    ) -> _IndexAccessor[ R ]:
        """Create a lazy accessor node."""
        return _IndexAccessor( self._factory, path, keys )

    def _traverse ( self, value: object, path: tuple[ str, ... ] = () ) -> object:
        """Convert parsed index data into an accessor tree."""

        keys = self._keys( value )
        if keys is not None:
            return self._create_index( keys, path )

        if isinstance( value, dict ):
            result: dict[ str, object ] = {}

            for key, child in value.items():
                if key == "$metadata":
                    continue

                result[ key ] = self._traverse( child, ( *path, key ) )

            return result

        return None

    async def get ( self ) -> object:
        """Return the lazily generated index tree."""
        return await self._transform( self._traverse )
