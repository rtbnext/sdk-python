"""TO BE IMPLEMENTED"""

from __future__ import annotations

from typing import Generic, TypeVar

R = TypeVar( "R" )
T = TypeVar( "T" )
U = TypeVar( "U" )


class CollectionBase( Generic[ T, R ] ):
    ...

class DateCollectionBase( CollectionBase[ T, R ], Generic[ T, R ] ):
    ...

class IndexCollectionBase( CollectionBase[ T, R ], Generic[ T, R ] ):
    ...
