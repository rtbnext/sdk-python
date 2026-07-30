"""
List

Declares types for ranking lists and snapshots.
"""

from typing import NotRequired, TypedDict

from rtbnext.schema.assets import ChangeItem
from rtbnext.schema.generic import ChangeFlag, Gender, Industry, MetaData, SelfMadeRank

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

ListItem = TypedDict( "ListItem", {
    "uri": NotRequired[ str ],
    "sourceUri": str,
    "name": str,
    "rank": int,
    "networth": NotRequired[ float ],
    "industry": NotRequired[ Industry ],
    "source": NotRequired[ list[ str ] ],
    "gender": NotRequired[ Gender ],
    "age": NotRequired[ int ],
    "citizenship": NotRequired[ str ],
    "flag": NotRequired[ ChangeFlag ],
    "rankDiff": NotRequired[ int ],
    "selfMadeRank": NotRequired[ SelfMadeRank ],
    "philanthropyScore": NotRequired[ int ]
} )

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
