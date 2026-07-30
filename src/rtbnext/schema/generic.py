"""
Literals & Generics

Declares literals and generic types.
"""

from typing import Literal, NotRequired, TypedDict

type Industry = Literal[
    "automotive", "diversified", "energy", "engineering", "finance", "foodstuff",
    "gambling", "healthcare", "logistics", "manufacturing", "media", "mining",
    "property", "retail", "service", "sports", "technology", "telecom"
]

type AgeGroup = Literal[ "30", "40", "50", "60", "70", "80", "90" ]
type Gender = Literal[ "m", "f", "d" ]
type MaritalStatus = Literal[
    "single", "relationship", "married", "remarried", "engaged", "separated",
    "divorced", "widowed"
]

type SelfMadeRank = Literal[ "1", "2", "3", "4", "5", "6", "7", "8", "9", "10" ]

type RelationType = Literal[ "person", "organization", "place", "unknown" ]
type AssetType = Literal[ "public", "private", "misc" ]
type ChangeFlag = Literal[ "up", "down", "unchanged", "new", "returned", "dropoff", "unknown" ]

type ChildrenGroup = Literal[ "none", "one", "two", "three", "four", "5-to-10", "over-10" ]
type Percentile = Literal[ "10th", "25th", "50th", "75th", "90th", "95th", "99th" ]
type WealthSpread = Literal[ "1", "2", "5", "10", "20", "50", "100", "200", "500", "1000" ]

type FilterSpecial = Literal[ "deceased", "dropOff", "family", "selfMade" ]
type FilterGroup = Literal[
    "industry", "citizenship", "country", "state", "gender", "age", "maritalStatus",
    "special"
]

type Service = Literal[ "profile", "list", "mover", "filter", "stats", "system" ]
type StatusFlag = Literal[ "healthy", "degraded", "maintenance", "outage", "unknown" ]
type ProfileStatusFlag = Literal[ "healthy", "invalid", "missing", "unknown" ]

MetaData = TypedDict( "MetaData", {
    "schemaVersion": Literal[ "2" ],
    "generator": str,
    "lastModified": str
} )

ChangeItem = TypedDict( "ChangeItem", {
    "value": float,
    "percent": float
} )

Location = TypedDict( "Location", {
    "country": str,
    "state": NotRequired[ str ],
    "city": NotRequired[ str ]
} )

Education = TypedDict( "Education", {
    "school": str,
    "degree": NotRequired[ str ]
} )

Organization = TypedDict( "Organization", {
    "name": str,
    "title": NotRequired[ str ]
} )

SelfMade = TypedDict( "SelfMade", {
    "type": NotRequired[ str ],
    "is": bool,
    "rank": NotRequired[ SelfMadeRank ]
} )

Relation = TypedDict( "Relation", {
    "type": RelationType,
    "name": str,
    "relation": NotRequired[ str ],
    "uri": NotRequired[ str ]
} )

Image = TypedDict( "Image", {
    "url": str,
    "credits": str,
    "file": str,
    "thumb": NotRequired[ str ],
    "caption": NotRequired[ str ],
    "desc": NotRequired[ str ],
    "date": NotRequired[ str ]
} )

Wiki = TypedDict( "Wiki", {
    "uri": str,
    "pageId": int,
    "refId": int,
    "confidence": float,
    "name": str,
    "lastModified": str,
    "summary": list[ str ],
    "sortKey": NotRequired[ str ],
    "wikidata": NotRequired[ str ],
    "desc": NotRequired[ str ],
    "image": NotRequired[ Image ]
} )
