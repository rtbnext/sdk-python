"""
Assets

Declares shared types for assets, net worth, rankings, performance metrics,
and historical financial data.
"""

from typing import Literal, Optional, TypedDict

from rtbnext.schema.generic import AssetType, ChangeFlag

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
    "shares": Optional[ float ],
    "price": float,
    "currency": str,
    "exRate": float
} )

Asset = TypedDict( "Asset", {
    "type": AssetType,
    "label": str,
    "value": Optional[ float ],
    "info": Optional[ AssetInfo ]
} )

DataPoint = TypedDict( "DataPoint", {
    "date": str,
    "networth": float,
    "rank": Optional[ int ]
} )

Extrema = TypedDict( "Extrema", {
    "high": Optional[ DataPoint ],
    "low": Optional[ DataPoint ]
} )

type Returns = dict[ ReturnsPeriod, ChangeItem ]

Performance = TypedDict( "Performance", {
    "extrema": Optional[ Extrema ],
    "returns": Optional[ Returns ]
} )

RankingHistoryItem = TypedDict( "RankingHistoryItem", {
    "date": str,
    "rank": Optional[ int ],
    "networth": Optional[ float ],
    "prev": Optional[ str ],
    "next": Optional[ str ]
} )

Ranking = TypedDict( "Ranking", {
    "list": str,
    "name": str,
    "date": str,
    "rank": Optional[ int ],
    "networth": Optional[ float ],
    "prev": Optional[ str ],
    "next": Optional[ str ],
    "history": Optional[ list[ RankingHistoryItem ] ]
} )

Realtime = TypedDict( "Realtime", {
    "date": str,
    "rank": Optional[ int ],
    "networth": Optional[ float ],
    "prev": Optional[ str ],
    "next": Optional[ str ],
    "today": Optional[ ChangeItem ],
    "ytd": Optional[ ChangeItem ]
} )

AnnualRecord = TypedDict( "AnnualRecord", {
    "first": int | float,
    "last": int | float,
    "diff": int | float,
    "flag": ChangeFlag,
    "mean": float,
    "median": float,
    "max": int | float,
    "min": int | float,
    "range": int | float,
    "stdDev": float
} )

Annual = TypedDict( "Annual", {
    "year": int,
    "rank": Optional[ AnnualRecord ],
    "networth": Optional[ AnnualRecord ]
} )
