"""
Stats

Declares statistical data, grouped statistics, historical trends,
demographic distributions, and wealth analysis.
"""

from typing import NotRequired, TypedDict

from rtbnext.schema.generic import (
    AgeGroup, ChangeFlag, ChangeItem, ChildrenGroup, Gender, Industry, MaritalStatus, MetaData,
    Percentile, SelfMadeRank, WealthSpread
)

StatsData = TypedDict( "StatsData", {
    "profiles": int,
    "days": int
} )

GlobalStats = TypedDict( "GlobalStats", {
    "$metadata": MetaData,
    "stats": StatsData,
    "date": str,
    "count": int,
    "total": float,
    "woman": int,
    "quota": float,
    "today": NotRequired[ ChangeItem ],
    "ytd": NotRequired[ ChangeItem ]
} )

DBStats = TypedDict( "DBStats", {
    "$metadata": MetaData,
    "files": int,
    "size": int
} )

HistoryItem = tuple[ str, int, float, int, float, float, float ]
History = list[ HistoryItem ]

AgePyramidGroup = TypedDict( "AgePyramidGroup", {
    "count": int,
    "decades": dict[ AgeGroup, int ],
    "max": int,
    "min": int,
    "mean": int
} )

ChildrenStats = TypedDict( "ChildrenStats", {
    "full": dict[ str, int ],
    "short": dict[ ChildrenGroup, int ]
} )

ProfileStats = TypedDict( "ProfileStats", {
    "$metadata": MetaData,
    "gender": dict[ Gender, int ],
    "maritalStatus": dict[ MaritalStatus, int ],
    "agePyramid": dict[ Gender, AgePyramidGroup ],
    "children": ChildrenStats,
    "selfMade": dict[ SelfMadeRank, int ],
    "philanthropyScore": dict[ str, int ]
} )

ScatterItem = TypedDict( "ScatterItem", {
    "uri": str,
    "name": str,
    "gender": Gender,
    "age": int,
    "networth": float
} )

Scatter = TypedDict( "Scatter", {
    "$metadata": MetaData,
    "count": int,
    "items": list[ ScatterItem ]
} )

WealthStats = TypedDict( "WealthStats", {
    "$metadata": MetaData,
    "decades": dict[ AgeGroup, float ],
    "gender": dict[ Gender, float ],
    "percentiles": dict[ Percentile, float ],
    "quartiles": tuple[ float, float, float ],
    "spread": dict[ WealthSpread, float ],
    "total": float,
    "max": float,
    "min": float,
    "mean": float,
    "median": float,
    "stdDev": float
} )

Top10Item = TypedDict( "Top10Item", {
    "uri": str,
    "rank": int,
    "networth": float,
    "flag": ChangeFlag
} )

Top10 = TypedDict( "Top10", {
    "$metadata": MetaData,
    "entries": dict[ str, list[ Top10Item ] ]
} )

StatsIndexFirst = TypedDict( "StatsIndexFirst", {
    "uri": str,
    "name": str,
    "rank": int,
    "networth": float
} )

StatsIndexItem = TypedDict( "StatsIndexItem", {
    "date": str,
    "count": int,
    "total": float,
    "woman": int,
    "quota": float,
    "today": NotRequired[ ChangeItem ],
    "ytd": NotRequired[ ChangeItem ],
    "first": StatsIndexFirst
} )

IndustryStatsIndex = TypedDict( "IndustryStatsIndex", {
    "$metadata": MetaData,
    "items": dict[ Industry, StatsIndexItem ]
} )

CitizenshipStatsIndex = TypedDict( "CitizenshipStatsIndex", {
    "$metadata": MetaData,
    "items": dict[ str, StatsIndexItem ]
} )
