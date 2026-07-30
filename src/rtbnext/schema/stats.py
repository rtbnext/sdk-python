"""
Stats

Declares statistical data, grouped statistics, historical trends,
demographic distributions, and wealth analysis.
"""

from typing import TypedDict

from rtbnext.schema.generic import (
    AgeGroup, Change, ChangeFlag, ChildrenGroup, Gender, Industry, MaritalStatus, MetaData,
    Percentile, WealthSpread
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
