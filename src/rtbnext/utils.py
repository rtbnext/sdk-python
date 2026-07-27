"""Implement utility methods."""


from __future__ import annotations

from datetime import datetime, timezone
import re


def sanitize ( value: object, delimiter: str = "-" ) -> str:
    """
    Sanitize a value for use as a normalized identifier.

    The value is converted to a string, trimmed, converted to lowercase,
    and all non-alphanumeric characters are replaced with the given delimiter.

    Args:
        value:
            Value to sanitize.
        delimiter:
            Replacement character for invalid characters.

    Returns:
        The sanitized string.
    """

    result = str( value ).strip().lower()
    result = re.sub( r"[^a-z0-9]+", delimiter, result )
    result = re.sub( rf"[{ re.escape( delimiter ) }]{{2,}}", delimiter, result )

    return result


def ymd ( value: object ) -> str:
    """
    Convert a value to an UTC date string, the returned format is ``YYYY-MM-DD``.

    Args:
        value:
            Value convertible to a date.

    Returns:
        UTC formatted date string.

    Raises:
        ValueError:
            If the value cannot be parsed.
    """

    text = str( value )

    try:
        date = datetime.fromisoformat( text.replace( "Z", "+00:00" ) )
    except ValueError:
        date = datetime.strptime( text, "%Y-%m-%d" )

    if date.tzinfo is None:
        date = date.replace( tzinfo= timezone.utc )

    return date.astimezone( timezone.utc ).strftime( "%Y-%m-%d" )
