from datetime import datetime
from unittest.mock import Mock

import pytest
from chronology.admin import ProposalInline
from chronology.apps import ChronologyConfig
from chronology.models import (
    Festival,
    Helper,
    Proposal,
    Room,
    TimeSlot,
    WaitList,
    default_json_field,
)
from crowd.models import User
from notice_board.models import Meeting


def test_proposal_inline_has_add_permission():
    inline = ProposalInline(Mock(), Mock())

    assert inline.has_add_permission(Mock(), Mock()) == False


def test_chronlogy_config():
    assert ChronologyConfig.name == "chronology"


@pytest.mark.parametrize(
    "model, kwargs, expected",
    (
        (Festival, {"name": "Konwencik"}, "Konwencik"),
        (Room, {"name": "Sala 301"}, "Sala 301"),
        (WaitList, {"name": "Sesje RPG"}, "Sesje RPG"),
        (
            TimeSlot,
            {
                "start_time": datetime(2020, 7, 1, 12, 0, 0),
                "end_time": datetime(2020, 7, 1, 13, 0, 0),
            },
            "From 2020-07-01 12:00:00 to 2020-07-01 13:00:00",
        ),
        (Helper, {"user": User(username="bob")}, "bob"),
        (Proposal, {"meeting": Meeting(name="Spotkanie")}, "Spotkanie"),
    ),
)
def test_str(model, kwargs, expected):
    assert str(model(**kwargs)) == expected


def test_default_json_field():
    assert default_json_field() == {}
