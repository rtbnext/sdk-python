"""
List

Declares types for ranking lists and snapshots.
"""

from typing import NotRequired, TypedDict

from rtbnext.schema.assets import ChangeItem
from rtbnext.schema.generic import MetaData

ListIndexItem = TypedDict( "ListIndexItem", {
    "uri": str,
    "name": str,
    "text": str,
    "shortName": str,
    "desc": str,
    "columns": list[ str ],
    "filters": list[ str ]
} )

ListIndex = TypedDict( "ListIndex", {
    "$metadata": MetaData,
    "count": int,
    "items": list[ ListIndexItem ]
} )

ListItem = TypedDict( "ListItem", {} )

ListStats = TypedDict( "ListStats", {
    "date": str,
    "count": int,
    "total": float,
    "woman": int,
    "quota": float,
    "today": NotRequired[ ChangeItem ]
} )

List = TypedDict( "List", {
    "$metadata": MetaData,
    "uri": str,
    "date": str,
    "count": int,
    "items": list[ ListItem ],
    "stats": ListStats
} )
