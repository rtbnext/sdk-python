"""
Parser

Implements the HTTP response body parser methods for simple text,
JSON responses and CSV data.
"""

import json
from typing import Any

from rtbnext.core.http_client import HttpResponse


class Parser:
    """
    Parses HTTP response bodies into text or objects.

    The parser validates the response status and ensures that
    the response contains data before decoding it.
    """

    @staticmethod
    def text( res: HttpResponse ) -> str:
        """Convert an HTTP response body to UTF-8 text."""

        if not res.ok:
            raise RuntimeError( f"Request failed with status { res.status }." )

        if not res.body:
            raise RuntimeError( "Response contains no data." )

        try:
            return res.body.decode()
        except Exception as exc:
            raise RuntimeError( f"Failed to decode response: { exc }" ) from exc

    @staticmethod
    def json( res: HttpResponse ) -> Any:
        """Parse an HTTP response body as JSON."""

        try:
            return json.loads( Parser.text( res ) )
        except Exception as exc:
            raise RuntimeError( f"Failed to parse JSON: { exc }" ) from exc
