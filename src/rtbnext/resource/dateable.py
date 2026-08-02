"""
Dateable Resource

Implements the resource wrapper for date-indexed endpoints.
"""

from __future__ import annotations

from typing import Callable, Generic, TypedDict, TypeVar

from rtbnext.core.loader import ResourceStateLoader
from rtbnext.core.parser import ParserFn
from rtbnext.resource.base import Resource
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


class DateableResource( Resource[ D ], Generic[ D, R ] ):
    """
    Resource wrapper for date-indexed endpoints.

    This class provides lazy traversal over API endpoints that are indexed by
    date values. It allows for convenient access to resources based on their
    date keys, while maintaining the underlying resource data.
    """

    def __init__(
        self, path: str, loader: ResourceStateLoader, parser: ParserFn[ D ], *,
        date: DateFn[ R ]
    ) -> None:
        super().__init__( path, loader, parser )
        self._date = date

    def _collect_dates( self, dates: list[ str ] ) -> DateCollection[ R ]:
        """Creates a date collection."""

        return DateCollection( dates, factory= self._date )
