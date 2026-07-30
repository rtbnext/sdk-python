"""
Assets

Declares shared types for assets, net worth, rankings, performance metrics,
and historical financial data.
"""

from typing import Literal, NotRequired, TypedDict

from rtbnext.schema.generic import AssetType

type ReturnsPeriod = Literal[
    "week", "month", "quarter", "halfYear", "year", "twoYear", "fiveYear"
]

ChangeItem = TypedDict( "ChangeItem", {
    "value": float,
    "percent": float
} )

AssetInfo = TypedDict( "AssetInfo", {
    "exchange": str,
    "ticker": str,
    "shares": NotRequired[ float ],
    "price": float,
    "currency": str,
    "exRate": float
} )

Asset = TypedDict( "Asset", {
    "type": AssetType,
    "label": str,
    "value": NotRequired[ float ],
    "info": NotRequired[ AssetInfo ]
} )

DataPoint = TypedDict( "DataPoint", {
    "date": str,
    "networth": float,
    "rank": NotRequired[ int ]
} )

Extrema = TypedDict( "Extrema", {
    "high": NotRequired[ DataPoint ],
    "low": NotRequired[ DataPoint ]
} )

type Returns = dict[ ReturnsPeriod, ChangeItem ]

Performance = TypedDict( "Performance", {
    "extrema": NotRequired[ Extrema ],
    "returns": NotRequired[ Returns ]
} )

RankingHistoryItem = TypedDict( "RankingHistoryItem", {
    "date": str,
    "rank": NotRequired[ int ],
    "networth": NotRequired[ float ],
    "prev": NotRequired[ str ],
    "next": NotRequired[ str ]
} )

Ranking = TypedDict( "Ranking", {
    "list": str,
    "name": str,
    "date": str,
    "rank": NotRequired[ int ],
    "networth": NotRequired[ float ],
    "prev": NotRequired[ str ],
    "next": NotRequired[ str ],
    "history": NotRequired[ list[ RankingHistoryItem ] ]
} )

Realtime = TypedDict( "Realtime", {
    "date": str,
    "rank": NotRequired[ int ],
    "networth": NotRequired[ float ],
    "prev": NotRequired[ str ],
    "next": NotRequired[ str ],
    "today": NotRequired[ ChangeItem ],
    "ytd": NotRequired[ ChangeItem ]
} )
