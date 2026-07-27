"""Implement utility methods."""


from __future__ import annotations

import re
from datetime import datetime, timezone


def sanitize ( value: object, delimiter: str = "-" ) -> str:
    """Sanitize a value for use as a normalized identifier."""

    result = str( value ).strip().lower()
    result = re.sub( r"[^a-z0-9]+", delimiter, result )
    result = re.sub( rf"[{ re.escape( delimiter ) }]{{2,}}", delimiter, result )
    return result


def ymd ( value: object ) -> str:
    """Convert a value to an UTC date string, the returned format is `YYYY-MM-DD`."""

    text = str( value )

    try:
        date = datetime.fromisoformat( text.replace( "Z", "+00:00" ) )
    except ValueError:
        date = datetime.strptime( text, "%Y-%m-%d" )

    if date.tzinfo is None:
        date = date.replace( tzinfo= timezone.utc )

    return date.astimezone( timezone.utc ).strftime( "%Y-%m-%d" )
