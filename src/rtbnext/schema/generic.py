"""
Generic

Declares generic types.
"""

from typing import Literal, TypedDict


"""Supported business sectors."""
type Industry = Literal[
    "automotive", "diversified", "energy", "engineering", "finance", "foodstuff",
    "gambling", "healthcare", "logistics", "manufacturing", "media", "mining",
    "property", "retail", "service", "sports", "technology", "telecom"
]

"""Supported gender values."""
type Gender = Literal[ "m", "f", "d" ]

"""Supported marital status values."""
type MaritalStatus = Literal[
    "single", "relationship", "married", "remarried", "engaged", "separated",
    "divorced", "widowed"
]

"""Supported age groups."""
type AgeGroup = Literal[ "30", "40", "50", "60", "70", "80", "90" ]

"""Self-made ranking from 1 (lowest) to 10 (highest)."""
type SelfMadeRank = Literal[ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" ]

"""Supported relation target types."""
type RelationType = Literal[ "person", "organization", "place", "unknown" ]

"""Supported asset ownership categories."""
type AssetType = Literal[ "public", "private", "misc" ]

"""Supported change indicators for rankings or statistics."""
type ChangeFlag = Literal[ "up", "down", "unchanged", "new", "returned", "dropoff", "unknown" ]

"""Supported child count groups."""
type ChildrenGroup = Literal[ "none", "one", "two", "three", "four", "5-to-10", "over-10" ]

type StatusFlag = Literal[ "healthy", "degraded", "maintenance", "outage", "unknown" ]

type Service = Literal[ "profile", "list", "mover", "filter", "stats", "system" ]


MetaData = TypedDict( "MetaData", {
    "schemaVersion": Literal[ "2" ],
    "generator": str,
    "lastModified": str
} )
