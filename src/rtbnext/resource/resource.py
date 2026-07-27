"""
RESOURCE

Implements the base resource wrapper for HTTP responses.
"""


from typing import Any


class Resource [ Any ]:
    """Resource class."""

    def valid ( self ) -> bool:
        return False
