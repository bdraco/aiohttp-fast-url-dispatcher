__version__ = "0.0.0"


from aiohttp import web
from aiohttp.web_urldispatcher import (
    AbstractResource,
    UrlDispatcher,
    UrlMappingMatchInfo,
)


class FastUrlDispatcher(UrlDispatcher):
    """UrlDispatcher that uses a dict lookup for resolving."""

    def __init__(self) -> None:
        """Initialize the dispatcher."""
        super().__init__()
        self._resource_index: dict[str, list[AbstractResource]] = {}

    def register_resource(self, resource: AbstractResource) -> None:
        """Register a resource."""
        super().register_resource(resource)
        canonical = resource.canonical
        if "{" in canonical:  # strip at the first { to allow for variables
            canonical = canonical.split("{")[0].rstrip("/")
        # There may be multiple resources for a canonical path
        # so we use a list to avoid falling back to a full linear search
        self._resource_index.setdefault(canonical, []).append(resource)

    async def resolve(self, request: web.Request) -> UrlMappingMatchInfo:
        """Resolve a request."""
        url_parts = request.rel_url.raw_parts
        resource_index = self._resource_index

        # Walk the url parts looking for candidates
        for i in range(len(url_parts), 0, -1):
            url_part = "/" + "/".join(url_parts[1:i])
            if (resource_candidates := resource_index.get(url_part)) is not None:
                for candidate in resource_candidates:
                    if (
                        match_dict := (await candidate.resolve(request))[0]
                    ) is not None:
                        return match_dict

        # Finally, fallback to the linear search
        return await super().resolve(request)


def attach_fast_url_dispatcher(
    app: web.Application, dispatcher: FastUrlDispatcher
) -> None:
    """Attach the fast url dispatcher to the app."""
    app._router = dispatcher
