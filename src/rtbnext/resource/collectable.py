"""
Collectable Resource

Implements the resource wrapper for collectable endpoints.
"""

from __future__ import annotations

from typing import Generic, TypedDict, TypeVar

from rtbnext.resource.base import Resource
from rtbnext.resource.collection import IndexCollectionBase


class CollectItem( TypedDict ):
    """Ensure `uri` is included in the dict."""

    uri: str


class CollectData[ T: CollectItem ]( TypedDict ):
    """Ensure `items` is a list of collect items."""

    items: list[ T ]


D = TypeVar( "D", bound= CollectData )
I = TypeVar( "I", bound= CollectItem )
E = TypeVar( "E" )


class CollectCollection( IndexCollectionBase[ I, E ], Generic[ I, E ] ):
    ...


class CollectableResource( Resource[ D ], Generic[ D, I, E ] ):
    ...
