"""
Profile

Declares profile records representing individuals, including personal
information, financial data, relationships, media, and historical statistics.
"""

from typing import Literal, NotRequired, TypedDict

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
    "desc": NotRequired[ str ],
    "image": NotRequired[ str ]
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
    "gender": NotRequired[ Gender ],
    "birthDate": NotRequired[ str ],
    "age": NotRequired[ int ],
    "birthCountry": NotRequired[ str ],
    "residenceCountry": NotRequired[ str ],
    "citizenship": NotRequired[ str ],
    "industry": NotRequired[ Industry ],
    "source": NotRequired[ list[ str ] ],
    "networth": NotRequired[ float ],
    "rank": NotRequired[ int ],
    "organization": NotRequired[ str ],
    "maritalStatus": NotRequired[ MaritalStatus ],
    "children": NotRequired[ int ],
    "philanthropyScore": NotRequired[ int ],
    "selfMade": NotRequired[ bool ],
    "selfMadeRank": NotRequired[ SelfMadeRank ],
    "wikidata": NotRequired[ str ],
    "status": NotRequired[ ProfileStatusFlag ],
    "score": NotRequired[ float ],
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
    "flags": NotRequired[ list[ str ] ]
} )

ProfileMeta = TypedDict( "ProfileMeta", {
    "schemaVersion": Literal[ "2" ],
    "generator": str,
    "lastModified": str,
    "lastLookup": NotRequired[ str ],
    "status": NotRequired[ ProfileStatus ]
} )

type ProfileHistoryItem = tuple[ str, int, float, float, float ]
type ProfileHistory = list[ ProfileHistoryItem ]

ProfileFlags = TypedDict( "ProfileFlags", {
    "deceased": NotRequired[ bool ],
    "family": NotRequired[ bool ],
    "dropOff": NotRequired[ bool ],
    "embargo": NotRequired[ bool ]
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
    "birthDate": NotRequired[ str ],
    "birthPlace": NotRequired[ Location ],
    "citizenship": NotRequired[ str ],
    "residence": NotRequired[ Location ],
    "maritalStatus": NotRequired[ MaritalStatus ],
    "children": NotRequired[ int ],
    "education": NotRequired[ list[ Education ] ],
    "industry": Industry,
    "source": list[ str ],
    "selfMade": NotRequired[ SelfMade ],
    "philanthropyScore": NotRequired[ int ],
    "organization": NotRequired[ Organization ]
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
    "realtime": NotRequired[ Realtime ],
    "performance": NotRequired[ Performance ],
    "ranking": list[ Ranking ],
    "annual": list[ Annual ],
    "assets": list[ Asset ],
    "wiki": NotRequired[ Wiki ]
} )
