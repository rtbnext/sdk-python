"""
Stats

Declares statistical data, grouped statistics, historical trends,
demographic distributions, and wealth analysis.
"""

from typing import TypedDict

from rtbnext.schema.generic import (
    AgeGroup, Change, ChangeFlag, ChildrenGroup, Gender, Industry, MaritalStatus, MetaData,
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
    "quota": float
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
    "mean": float
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
