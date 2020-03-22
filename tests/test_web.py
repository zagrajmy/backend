# pylint: disable=redefined-outer-name
from unittest.mock import Mock

import pytest
from starlette.requests import Request

from zagrajmy.events import EventRegistry
from zagrajmy.web import EventHub

PAYLOAD = {
    "event": {
        "session_variables": {"x-hasura-role": "admin"},
        "op": "INSERT",
        "data": {"old": None, "new": {"name": "ssss", "id": 3}},
    },
    "created_at": "2020-03-18T18:42:07.30702Z",
    "id": "03ad9db7-a86e-4680-bae1-54f24775a519",
    "delivery_info": {"max_retries": 0, "current_retry": 0},
    "trigger": {"name": "test-event"},
    "table": {"schema": "public", "name": "nb_sphere"},
}


@pytest.fixture
def event_registry():
    registry = Mock(EventRegistry)

    async def run(data):
        assert data == PAYLOAD["event"]

    registry.get_event_class()().run = run
    return registry


@pytest.fixture
def json_request():
    async def json():
        return PAYLOAD

    json_request = Mock(Request)
    json_request.json = json
    return json_request


@pytest.fixture
def graphql_client():
    graphql_client = Mock()
    return graphql_client


@pytest.mark.asyncio
async def test_eventhub(event_registry, graphql_client, json_request):
    event_hub = EventHub(event_registry=event_registry, graphql_client=graphql_client)
    response = await event_hub.call(json_request)

    assert response.body == b'{"message":"success"}'
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_eventhub_validation_error(event_registry, graphql_client):
    event_hub = EventHub(event_registry=event_registry, graphql_client=graphql_client)
    json_request = Mock(Request)

    async def wrong_json():
        return {"wrong": "data"}

    json_request.json = wrong_json
    response = await event_hub.call(json_request)

    assert response.body == b"{\"message\":\"{'wrong': ['Unknown field.']}\"}"
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_eventhub_event_not_found(json_request, graphql_client):
    event_hub = EventHub(event_registry=EventRegistry, graphql_client=graphql_client)
    response = await event_hub.call(json_request)

    assert response.body == b'{"message":"Event not found: test-event"}'
    assert response.status_code == 400
