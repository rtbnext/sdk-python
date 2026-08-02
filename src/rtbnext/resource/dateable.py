"""
Dateable Resource

Implements the resource wrapper for date-indexed endpoints.
"""

from __future__ import annotations

from typing import Callable, Generic, TypedDict, TypeVar

from rtbnext.resource.collection import DateCollectionBase


class DateData( TypedDict ):
    """Ensure `dates` is included in the dict."""

    dates: list[ str ]

D = TypeVar( "D", bound= DateData )
R = TypeVar( "R" )

type DateFn[ R ] = Callable[ [ str ], R ]


class DateCollection( DateCollectionBase[ str, R ], Generic[ R ] ):
    """
    Collection wrapper for date-indexed resources.

    This class provides convenient filtering and mapping operations for resources
    that are indexed by date values. It allows for lazy resolution of resources
    based on their date keys, while maintaining the underlying collection of date
    strings.
    """
