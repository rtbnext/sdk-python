"""
Collectable Resource

Implements the resource wrapper for collectable endpoints.
"""

from typing import Callable, TypedDict, TypeVar


class CollectItem( TypedDict ):
    """Ensure `uri` is included in the dict."""

    uri: str


class CollectData[ T: CollectItem ]( TypedDict ):
    """Ensure `items` is a list of collect items."""

    items: list[ T ]

K = TypeVar( "K" )
T = TypeVar( "T", bound= dict )
R = TypeVar( "R" )

type FindFn[ T ] = Callable[ [ list[ T ], str ], T | None ]
type SearchFn[ T ] = Callable[ [ T, str, list[ str ] ], bool ]
