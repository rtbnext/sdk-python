"""
Profile

Declares profile records representing individuals, including personal
information, financial data, relationships, media, and historical statistics.
"""

from typing import Literal, Optional, TypedDict

from rtbnext.schema.assets import Annual, Asset, Performance, Ranking, Realtime
from rtbnext.schema.generic import (
    Education, Gender, Image, Industry, Location, MaritalStatus, MetaData, Organization,
    ProfileStatusFlag, Relation, SelfMade, SelfMadeRank, Wiki
)

ProfileIndexItem = TypedDict( "ProfileIndexItem", {
    "uri": str,
    "name": str,
    "text": str,
    "aliases": list[ str ],
    "desc": Optional[ str ],
    "image": Optional[ str ]
} )

ProfileIndex = TypedDict( "ProfileIndex", {
    "$metadata": MetaData,
    "count": int,
    "items": list[ ProfileIndexItem ]
} )

SearchIndexItem = TypedDict( "SearchIndexItem", {
    "id": str,
    "uri": str,
    "deceased": bool,
    "family": bool,
    "dropOff": bool,
    "embargo": bool,
    "searchName": str,
    "fullName": str,
    "lastName": str,
    "gender": Optional[ Gender ],
    "birthDate": Optional[ str ],
    "age": Optional[ int ],
    "birthCountry": Optional[ str ],
    "residenceCountry": Optional[ str ],
    "citizenship": Optional[ str ],
    "industry": Optional[ Industry ],
    "source": Optional[ list[ str ] ],
    "networth": Optional[ float ],
    "rank": Optional[ int ],
    "organization": Optional[ str ],
    "maritalStatus": Optional[ MaritalStatus ],
    "children": Optional[ int ],
    "philanthropyScore": Optional[ int ],
    "selfMade": Optional[ bool ],
    "selfMadeRank": Optional[ SelfMadeRank ],
    "wikidata": Optional[ str ],
    "status": Optional[ ProfileStatusFlag ],
    "score": Optional[ float ],
    "timestamp": str
} )

SearchIndex = TypedDict( "SearchIndex", {
    "$metadata": MetaData,
    "count": int,
    "items": list[ SearchIndexItem ]
} )

ProfileStatus = TypedDict( "ProfileStatus", {
    "status": ProfileStatusFlag,
    "score": float,
    "flags": Optional[ list[ str ] ]
} )

ProfileMeta = TypedDict( "ProfileMeta", {
    "schemaVersion": Literal[ "2" ],
    "generator": str,
    "lastModified": str,
    "lastLookup": Optional[ str ],
    "status": Optional[ ProfileStatus ]
} )

type ProfileHistoryItem = tuple[ str, int, float, float, float ]
type ProfileHistory = list[ ProfileHistoryItem ]

ProfileFlags = TypedDict( "ProfileFlags", {
    "deceased": Optional[ bool ],
    "family": Optional[ bool ],
    "dropOff": Optional[ bool ],
    "embargo": Optional[ bool ]
} )

ProfileName = TypedDict( "ProfileName", {
    "fullName": str,
    "shortName": str,
    "lastName": str,
    "firstName": str
} )

ProfileInfo = TypedDict( "ProfileInfo", {
    "flags": ProfileFlags,
    "name": ProfileName,
    "gender": Gender,
    "birthDate": Optional[ str ],
    "birthPlace": Optional[ Location ],
    "citizenship": Optional[ str ],
    "residence": Optional[ Location ],
    "maritalStatus": Optional[ MaritalStatus ],
    "children": Optional[ int ],
    "education": Optional[ list[ Education ] ],
    "industry": Industry,
    "source": list[ str ],
    "selfMade": Optional[ SelfMade ],
    "philanthropyScore": Optional[ int ],
    "organization": Optional[ Organization ]
} )

ProfileBio = TypedDict( "ProfileBio", {
    "cv": list[ str ],
    "quotes": list[ str ],
    "facts": list[ str ]
} )

ProfileData = TypedDict( "ProfileData", {
    "id": str,
    "uri": str,
    "info": ProfileInfo,
    "bio": ProfileBio,
    "related": list[ Relation ],
    "media": list[ Image ],
    "realtime": Optional[ Realtime ],
    "performance": Optional[ Performance ],
    "ranking": list[ Ranking ],
    "annual": list[ Annual ],
    "assets": list[ Asset ],
    "wiki": Optional[ Wiki ]
} )
