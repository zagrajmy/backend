import os
from distutils.util import strtobool
from typing import Type

from marshmallow.exceptions import ValidationError
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from .events import EventNotFound, EventRegistry
from .hasura_client import HasuraClient
from .schemas import PayloadSchema


class EventHub:
    """Master view of event handlers."""

    def __init__(
        self, event_registry: Type[EventRegistry], graphql_client: HasuraClient
    ) -> None:
        """Create event hub with chosen event executor."""
        self._event_registry = event_registry
        self._graphql_client = graphql_client

    async def call(self, request: Request) -> JSONResponse:
        """Call event and return status."""
        body = await request.json()

        try:
            body = PayloadSchema().load(body)
        except ValidationError as exception:
            return JSONResponse({"message": str(exception)}, status_code=400)

        trigger = body["trigger"]["name"]
        try:
            event_class = self._event_registry.get_event_class(trigger)
        except EventNotFound as exception:
            return JSONResponse({"message": str(exception)}, status_code=400)

        await event_class(self._graphql_client).run(body["event"])

        return JSONResponse({"message": "success"})


HASURA = HasuraClient(
    url="http://graphql-engine:8080/v1/graphql",
    auth={"x-hasura-admin-secret": "dev_only_password"},
)


APP = Starlette(
    debug=strtobool(os.getenv("DEBUG", "no")),
    routes=[Route("/events", EventHub(EventRegistry, HASURA).call, methods=["POST"])],
)
