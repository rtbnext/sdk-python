"""
Utils

Implements utility methods.
"""


from __future__ import annotations

import re
from datetime import datetime, timezone


def sanitize( value: object, delimiter: str = "-" ) -> str:
    """Sanitize a value for use as a normalized identifier."""

    result = str( value ).strip().lower()
    result = re.sub( r"[^a-z0-9]+", delimiter, result )
    result = re.sub( rf"[{ re.escape( delimiter ) }]{{2,}}", delimiter, result )

    return result


def ymd( value: object ) -> str:
    """Convert a value to a UTC date string `YYYY-MM-DD`."""

    text = str( value )

    try:
        dt = datetime.fromisoformat( text.replace( "Z", "+00:00" ) )
    except ValueError:
        dt = datetime.strptime( text, "%Y-%m-%d" )

    if not dt.tzinfo:
        dt = dt.replace( tzinfo= timezone.utc )

    return dt.astimezone( timezone.utc ).strftime( "%Y-%m-%d" )
