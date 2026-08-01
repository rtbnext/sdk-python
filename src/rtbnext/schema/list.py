"""
List

Declares types for ranking lists and snapshots.
"""

from typing import Optional, TypedDict

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
    "uri": Optional[ str ],
    "sourceUri": str,
    "name": str,
    "rank": int,
    "networth": Optional[ float ],
    "industry": Optional[ Industry ],
    "source": Optional[ list[ str ] ],
    "gender": Optional[ Gender ],
    "age": Optional[ int ],
    "citizenship": Optional[ str ],
    "flag": Optional[ ChangeFlag ],
    "rankDiff": Optional[ int ],
    "selfMadeRank": Optional[ SelfMadeRank ],
    "philanthropyScore": Optional[ int ],
    "today": Optional[ ChangeItem ],
    "ytd": Optional[ ChangeItem ]
} )

ListStats = TypedDict( "ListStats", {
    "date": str,
    "count": int,
    "total": float,
    "woman": int,
    "quota": float,
    "today": Optional[ ChangeItem ],
    "ytd": Optional[ ChangeItem ]
} )

List = TypedDict( "List", {
    "$metadata": MetaData,
    "uri": str,
    "date": str,
    "count": int,
    "items": list[ ListItem ],
    "stats": ListStats
} )
