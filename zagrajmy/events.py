"""Actions and paths for API views."""
from typing import Any, Dict, Tuple, Type, TypedDict

from .hasura_client import HasuraClient


class EventData(TypedDict):
    """Typed dict describing event data."""

    session_variables: Dict[str, str]
    op: str
    data: Dict[str, Dict[str, Any]]


class EventNotFound(Exception):
    """Error for not existing event trigger."""


class EventRegistry(type):
    """Event registry and metaclass."""

    events: Dict[str, Type["EventBase"]] = {}

    def __new__(  # type: ignore
        cls, name: str, bases: Tuple[type, ...], attrs: Dict[str, str]
    ) -> Any:
        """Add a new subclass to events registry."""
        new_cls: Type["EventBase"] = super().__new__(cls, name, bases, attrs)
        cls.events[new_cls.TRIGGER] = new_cls
        return new_cls

    @classmethod
    def get_event_class(cls, trigger: str) -> Type["EventBase"]:
        """Check if event exists and run it."""
        if trigger not in cls.events:
            raise EventNotFound(f"Event not found: {trigger}")
        return cls.events[trigger]


class EventBase(metaclass=EventRegistry):
    """Base class for all event handlers."""

    TRIGGER: str = ""

    def __init__(self, graphql_client: HasuraClient) -> None:
        """Initialize event with data from payload."""
        self._graphql_client = graphql_client

    async def run(self, event_data: EventData) -> None:
        """Run event action."""


class SphereCreatedEvent(EventBase):
    """Create default guild when a sphere is created."""

    TRIGGER = "sphere_created"

    async def run(self, event_data: EventData) -> None:
        """Create default guild for a new sphere."""
        name = event_data["data"]["new"]["name"]
        await self._graphql_client.insert_guild(
            name="DEFAULT", description=f"Default guild for sphere {name}",
        )
