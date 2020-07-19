from datetime import datetime
from unittest.mock import Mock

import pytest

from chronology import models
from chronology.admin import ProposalInline
from chronology.apps import ChronologyConfig
from crowd.models import User


def test_proposal_inline_has_add_permission():
    inline = ProposalInline(Mock(), Mock())

    assert inline.has_add_permission(Mock(), Mock()) is False


def test_chronlogy_config():
    assert ChronologyConfig.name == "chronology"


@pytest.mark.parametrize(
    "model, kwargs, expected",
    (
        (models.Festival, {"name": "Konwencik"}, "Konwencik"),
        (models.Room, {"name": "Sala 301", "id": 7}, "Sala 301 (7)"),
        (models.WaitList, {"name": "Sesje RPG", "id": 8}, "Sesje RPG (8)"),
        (
            models.TimeSlot,
            {
                "start_time": datetime(2020, 7, 1, 12, 0, 0),
                "end_time": datetime(2020, 7, 1, 13, 0, 0),
                "id": 9,
            },
            "From 2020-07-01 12:00:00 to 2020-07-01 13:00:00 (9)",
        ),
        (models.Helper, {"user": User(username="bob")}, "bob"),
        (models.Proposal, {"name": "Spotkanie"}, "Spotkanie"),
    ),
)
def test_str(model, kwargs, expected):
    assert str(model(**kwargs)) == expected


def test_default_json_field():
    assert models.default_json_field() == {}
