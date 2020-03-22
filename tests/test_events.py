# pylint: disable=redefined-outer-name
from unittest.mock import Mock

import pytest

from zagrajmy.events import EventNotFound, EventRegistry


@pytest.fixture
def empty_event_base():
    old_events = EventRegistry.events
    EventRegistry.events = {}
    yield EventRegistry
    EventRegistry.events = old_events


@pytest.fixture
def graphql_client():
    graphql_client = Mock()

    async def insert_guild(name, description):
        graphql_client.args = {"name": name, "description": description}

    graphql_client.insert_guild = insert_guild
    return graphql_client


def test_event_manager(empty_event_base):
    example_event_class = empty_event_base(
        "ExampleEvent", (), {"TRIGGER": "example-event"},
    )

    assert empty_event_base.events == {"example-event": example_event_class}


def test_get_event_class_error():
    with pytest.raises(EventNotFound):
        EventRegistry.get_event_class("not-an-event")


def test_get_event_class(empty_event_base):
    example_event_class = empty_event_base(
        "ExampleEvent", (), {"TRIGGER": "example-event"},
    )

    assert empty_event_base.get_event_class("example-event") == example_event_class


@pytest.mark.asyncio
async def test_sphere_created(graphql_client):
    sphere_created_class = EventRegistry.get_event_class("sphere_created")
    sphere_created = sphere_created_class(graphql_client=graphql_client)
    await sphere_created.run({"data": {"new": {"name": "test-sphere"}}})

    assert graphql_client.args == dict(
        name="DEFAULT", description="Default guild for sphere test-sphere",
    )
