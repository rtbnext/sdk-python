"""
List

Declares types for ranking lists and snapshots.
"""

from typing import TypedDict

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
