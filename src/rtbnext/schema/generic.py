from typing import Literal, TypedDict

type StatusFlag = Literal[ "healthy", "degraded", "maintenance", "outage", "unknown" ]
type Service = Literal[ "profile", "list", "mover", "filter", "stats", "system" ]


MetaData = TypedDict( "MetaData", {
    "schemaVersion": Literal[ "2" ],
    "generator": str,
    "lastModified": str
} )
