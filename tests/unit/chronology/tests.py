from unittest.mock import Mock

import pytest
from django.core.exceptions import ValidationError

from chronology import models as chronology_models
from chronology.admin import ProposalInline
from chronology.apps import ChronologyConfig
from chronology.models import AgendaItem, Festival, TimeSlot
from chronology.templatetags.agenda import agenda_cell
from crowd.models import User
from tests.factories import (
    AgendaItemFactory,
    FestivalFactory,
    HelperFactory,
    MeetingFactory,
    ProposalFactory,
    RoomFactory,
)


def test_proposal_inline_has_add_permission():
    inline = ProposalInline(Mock(), Mock())

    assert inline.has_add_permission(Mock(), Mock()) is False


def test_chronlogy_config():
    assert ChronologyConfig.name == "chronology"


@pytest.mark.parametrize(
    "model, kwargs, expected",
    (
        (Festival, {"name": "Konwencik"}, "Konwencik"),
        (chronology_models.Room, {"name": "Sala 301", "id": 7}, "Sala 301 (7)"),
        (chronology_models.WaitList, {"name": "Sesje RPG", "id": 8}, "Sesje RPG (8)"),
        (
            TimeSlot,
            {"start_time": 4, "end_time": 5, "id": 9},
            "From 2020-08-01 14:00:00+00:00 to 2020-08-01 15:00:00+00:00 (9)",
        ),
        (chronology_models.Helper, {"user": User(username="bob")}, "bob"),
        (chronology_models.Proposal, {"name": "Spotkanie"}, "Spotkanie"),
    ),
)
def test_str(hour, model, kwargs, expected):
    if kwargs.get("start_time") and kwargs.get("end_time"):
        kwargs["start_time"] = hour(kwargs.get("start_time"))
        kwargs["end_time"] = hour(kwargs.get("end_time"))

    assert str(model(**kwargs)) == expected


def test_default_json_field():
    assert chronology_models.default_json_field() == {}


@pytest.mark.django_db
def test_festival_draft():
    festival = FestivalFactory(
        end_proposal=None,
        end_time=None,
        start_proposal=None,
        start_publication=None,
        start_time=None,
    )
    assert festival.status == Festival.DRAFT


@pytest.mark.parametrize(
    "start_time,end_time", ((-1, 1), (1, 3), (3, 5), (-1, 5)),
)
@pytest.mark.django_db
def test_timeslot_validate_unique_error(hour, start_time, end_time):
    festival = FestivalFactory()
    TimeSlot.objects.create(
        festival=festival, start_time=hour(start_time), end_time=hour(end_time)
    )

    with pytest.raises(ValidationError) as exc:
        TimeSlot.objects.create(
            festival=festival, start_time=hour(0), end_time=hour(4),
        )

    assert str(exc.value) == "{'__all__': [\"Time slots can't overlap!\"]}"


@pytest.mark.django_db
def test_timeslot_validate_unique_different_festival(hour):
    festival1 = FestivalFactory()
    festival2 = FestivalFactory()
    TimeSlot.objects.create(festival=festival1, start_time=hour(0), end_time=hour(4))
    TimeSlot.objects.create(festival=festival2, start_time=hour(0), end_time=hour(4))


@pytest.mark.parametrize(
    "start_time,end_time", ((-4, -1), (-4, 0), (4, 5), (5, 7)),
)
@pytest.mark.django_db
def test_timeslot_validate_unique(hour, start_time, end_time):
    festival = FestivalFactory()
    TimeSlot.objects.create(
        festival=festival, start_time=hour(start_time), end_time=hour(end_time)
    )

    TimeSlot.objects.create(
        festival=festival, start_time=hour(0), end_time=hour(4),
    )


@pytest.mark.parametrize(
    "kwargs,status",
    (
        ({"helper": None}, AgendaItem.UNASSIGNED),
        (
            {"meeting_confirmed": True, "helper_confirmed": False},
            AgendaItem.UNCONFIRMED,
        ),
        (
            {"meeting_confirmed": False, "helper_confirmed": True},
            AgendaItem.UNCONFIRMED,
        ),
        ({"meeting_confirmed": True, "helper_confirmed": True}, AgendaItem.CONFIRMED),
    ),
)
@pytest.mark.django_db
def test_agenda_item_status(kwargs, status):
    festival = FestivalFactory()
    base_kwargs = {
        "helper": HelperFactory(festival=festival),
        "room": RoomFactory(festival=festival),
        "meeting": MeetingFactory(),
        "meeting_confirmed": False,
        "helper_confirmed": False,
    }
    base_kwargs.update(kwargs)

    agenda_item = AgendaItem.objects.create(**base_kwargs)

    assert agenda_item.status == status


@pytest.mark.django_db
def test_agenda_item_str():
    proposal = ProposalFactory(
        speaker_name="John Gale", meeting=MeetingFactory(name="About my game")
    )
    agenda_item = AgendaItemFactory(meeting=proposal.meeting)

    assert str(agenda_item) == "About my game by John Gale (unassigned)"


@pytest.mark.django_db
def test_agenda_cell(hour):
    context = agenda_cell(room=RoomFactory(), hour=hour(0))

    context.pop("rendered_widget")
    assert context == {
        "add_related_url": "/admin/chronology/agendaitem/add/",
        "can_add_related": True,
        "can_change_related": True,
        "can_delete_related": True,
        "change_related_template_url": "/admin/chronology/agendaitem/__fk__/change/",
        "delete_related_template_url": "/admin/chronology/agendaitem/__fk__/delete/",
        "is_hidden": False,
        "model": "agenda item",
        "name": "agendaitem_r1_t2020-08-01-10-00-00-000000-UTC",
        "url_params": (
            "_to_field=id&_popup=1&room=1&hour=2020-08-01-10-00-00-000000-UTC"
        ),
    }
