"""
Dateable Resource

Implements the resource wrapper for date-indexed endpoints
"""

from typing import Generic, TypedDict, TypeVar

from rtbnext.resource.collection import DateCollectionBase


class DateData( TypedDict ):
    """Ensure `dates` is included in the dict."""

    dates: list[ str ]

D = TypeVar( "D", bound= DateData )
R = TypeVar( "R" )


class DateCollection( DateCollectionBase[ R ], Generic[ R ] ):
    """
    Collection wrapper for date-indexed resources.

    This class provides convenient filtering and mapping operations for resources
    that are indexed by date values. It allows for lazy resolution of resources
    based on their date keys, while maintaining the underlying collection of date
    strings.
    """
