"""Implement utility methods."""


from __future__ import annotations

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
