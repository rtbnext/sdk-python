"""
Dateable Resource

Implements the resource wrapper for date-indexed endpoints
"""

from typing import Generic, TypedDict, TypeVar, Callable

from rtbnext.resource.collection import DateCollectionBase
from rtbnext.resource.base import Resource
from rtbnext.core.resource import ResourceLoader
from rtbnext.core.parser import ParserFn


class DateData( TypedDict ):
    """Ensure `dates` is included in the dict."""

    dates: list[ str ]

D = TypeVar( "D", bound= DateData )
R = TypeVar( "R" )
type DateFn[ R ] = Callable[ [ str ], R ]


class DateCollection( DateCollectionBase[ R ], Generic[ R ] ):
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
        self,
        path: str,
        loader: ResourceLoader,
        parser: ParserFn[ D ],
        date: DateFn[ R ]
    ):
        super().__init__( path, loader, parser )
        self._factory = date
