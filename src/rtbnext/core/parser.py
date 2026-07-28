"""
Parser

Implements the HTTP response body parser methods for simple text,
JSON responses and CSV data.
"""

class Parser:
    """
    Parses HTTP response bodies into text or objects.

    The parser validates the response status and ensures that
    the response contains data before decoding it.
    """
