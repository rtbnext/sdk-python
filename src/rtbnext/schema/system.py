from typing import TypedDict

from rtbnext.schema.generic import MetaData, Service, StatusFlag


SystemStatus = TypedDict( "SystemStatus", {
    "$metadata": MetaData,
    "status": StatusFlag,
    "services": dict[ Service, StatusFlag ]
} )
