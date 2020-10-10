from functools import partial

import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework.test import APIClient

from chronology.models import Proposal
from tests.factories import ProposalFactory, UserFactory, WaitListFactory


@pytest.fixture
def user(db):
    return UserFactory(
        first_name="Mszczuj", last_name="ze Skzynna", username="PanMszczuj"
    )


@pytest.fixture
def post_proposal_list():
    client = APIClient()
    return partial(client.post, reverse("v1:chronology:proposals-list"))


@pytest.fixture
def waitlist(db):
    return WaitListFactory()


@pytest.mark.parametrize("speaker_field", ("speaker_name", "speaker_user"))
@freeze_time("2020-07-04")
def test_create(waitlist, speaker_field, post_proposal_list, user):
    time_slot_ids = [t_s.id for t_s in waitlist.festival.time_slots.all()]
    speaker_value = (
        str(user.uuid) if speaker_field == "speaker_user" else "Mszczuj ze Skzynna"
    )

    res = post_proposal_list(
        data={
            "city": "Toruń",
            "club": "A",
            "duration_minutes": 600,
            "name": "O obrotach sfer niebieskich",
            "needs": "no",
            "phone": "+4812",
            "time_slots": time_slot_ids,
            "topic": "Literature",
            "waitlist": waitlist.id,
            speaker_field: speaker_value,
        }
    )

    res_data = res.json()
    proposal = Proposal.objects.first()
    if speaker_field == "speaker_user":
        assert (
            str(proposal.speaker_user.uuid)
            == res_data.pop("speaker_user")
            == str(user.uuid)
        )
    else:
        assert proposal.speaker_user is res_data.pop("speaker_user") is None

    assert (
        list(proposal.time_slots.values_list("id", flat=True))
        == res_data.pop("time_slots")
        == time_slot_ids
    )
    assert proposal.city == res_data.pop("city") == "Toruń"
    assert proposal.club == res_data.pop("club") == "A"
    assert proposal.description == res_data.pop("description") == ""
    assert proposal.duration_minutes == res_data.pop("duration_minutes") == 600
    assert proposal.id == res_data.pop("id") == 1
    assert proposal.meeting is res_data.pop("meeting") is None
    assert proposal.name == res_data.pop("name") == "O obrotach sfer niebieskich"
    assert proposal.needs == res_data.pop("needs") == "no"
    assert proposal.other_contact == res_data.pop("other_contact") == {}
    assert proposal.other_data == res_data.pop("other_data") == {}
    assert proposal.phone == res_data.pop("phone") == "+4812"
    assert proposal.speaker_name == res_data.pop("speaker_name") == "Mszczuj ze Skzynna"
    assert proposal.status == res_data.pop("status") == "CREATED"
    assert proposal.topic == res_data.pop("topic") == "Literature"
    assert proposal.waitlist.id == res_data.pop("waitlist") == 1

    assert res_data == {}


@freeze_time("2020-07-04")
def test_create_no_user_data_error(post_proposal_list, waitlist):
    res = post_proposal_list(
        data={
            "name": "O obrotach sfer niebieskich",
            "duration_minutes": 600,
            "city": "Toruń",
            "club": "A",
            "phone": "+4812",
            "needs": "no",
            "waitlist": waitlist.id,
            "time_slots": [t_s.id for t_s in waitlist.festival.time_slots.all()],
        },
    )
    res_data = res.json()
    assert res_data["non_field_errors"] == ["No speaker name nor speaker user"]


@freeze_time("2020-07-04")
def test_update(waitlist):
    proposal = ProposalFactory(
        name="Lightning talk", speaker_name="B. Franklin", waitlist=waitlist
    )
    res = APIClient().patch(
        reverse("v1:chronology:proposals-detail", kwargs={"id": proposal.id}),
        data={"speaker_name": "N. Tesla"},
    )
    res_data = res.json()
    proposal.refresh_from_db()
    assert proposal.speaker_name == "N. Tesla"
    assert res_data.get("speaker_name") == "N. Tesla"
