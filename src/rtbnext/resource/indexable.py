"""Implement the resource wrapper for nested indexable endpoints."""


from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, cast

from rtbnext.core.http_client import HttpResponse
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
        """
        Create a lazy index accessor.

        Args:
            factory:
                Resource resolver.
            path:
                Current traversal path.
            keys:
                Available child keys.
        """

        self._factory = factory
        self._path = path
        self._keys = keys


    def __getattr__ ( self, key: str ) -> R:
        """
        Resolve a nested resource.

        Args:
            key:
                Index key.

        Returns:
            The resolved resource.

        Raises:
            AttributeError:
                If the key does not exist.
        """

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
        """
        Create a new indexable resource.

        Args:
            path:
                API resource path.
            loader:
                Resource loader used for fetching data.
            parser:
                Parser used to decode responses.
            options:
                Index traversal configuration.
        """

        super().__init__( path, loader, parser )

        self._factory = options.index
        self._keys = options.keys or self._default_keys

    @staticmethod
    def _default_keys ( value: object ) -> tuple[ str, ... ] | None:
        """
        Extract index keys from common API structures.

        Supports:
        - lists of keys
        - objects containing an ``items`` mapping

        Args:
            value:
                Parsed resource value.

        Returns:
            Available keys or ``None``.
        """

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
        """
        Create a lazy accessor node.

        Args:
            keys:
                Available child keys.
            path:
                Current traversal path.

        Returns:
            Lazy accessor instance.
        """

        return _IndexAccessor( self._factory, path, keys )
