from rtbnext.core.http_client import ClientIdentity
from rtbnext.core.resource import CacheMode, CacheType


class RTBNext:
    """
    Main entry point of the RTBNext SDK.

    Provides access to all RTBNext API endpoints through a single client
    instance while internally managing HTTP communication, resource loading,
    caching, and endpoint initialization.
    """

    def __init__(
        self, client: ClientIdentity, *,
        base_url: str | None = None,
        timeout: float | None = None,
        cache: CacheType | None = None,
        mode: CacheMode | None = None
    ) -> None:
        ...
