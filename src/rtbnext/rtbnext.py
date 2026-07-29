from rtbnext.core.http_client import ClientIdentity, HttpClient
from rtbnext.core.resource import CacheMode, CacheType
from rtbnext.defaults import DEFAULT_API_URL, DEFAULT_TIMEOUT


class RTBNext:
    """
    Main entry point of the RTBNext SDK.

    Provides access to all RTBNext API endpoints through a single client
    instance while internally managing HTTP communication, resource loading,
    caching, and endpoint initialization.
    """

    def __init__(
        self, client: ClientIdentity, *,
        base_url: str = DEFAULT_API_URL,
        timeout: float = DEFAULT_TIMEOUT,
        cache: CacheType | None = None,
        mode: CacheMode | None = None
    ) -> None:
        self._http_client = HttpClient( client= client, base_url= base_url, timeout= timeout )
