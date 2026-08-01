"""
Utils

Implements internal used utility methods.
"""

from __future__ import annotations

import re


def sanitize( value: object, delimiter: str = "-" ) -> str:
    """Sanitize a value for use as a normalized identifier."""

    result = str( value ).strip().lower()
    result = re.sub( r"[^a-z0-9]+", delimiter, result )
    result = re.sub( rf"[{ re.escape( delimiter ) }]{{2,}}", delimiter, result )

    return result
