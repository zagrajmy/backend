from django.urls import reverse
from freezegun import freeze_time
from rest_framework.test import APITestCase

from crowd.models import User
from chronology.models import Proposal

from tests.factories import (
    FestivalFactory,
    ProposalFactory,
    TimeSlotFactory,
    WaitListFactory,
)


class TestProposals(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Mszczuj", last_name="ze Skzynna", username="PanMszczuj"
        )
        self.proposals_url = reverse("v1:chronology:proposals-list")
        self.festival = FestivalFactory()
        self.wait_list = WaitListFactory(festival=self.festival)
        self.time_slots = [
            TimeSlotFactory(festival=self.festival),
            TimeSlotFactory(festival=self.festival),
        ]

    @freeze_time("2020-07-04")
    def test_create(self):
        res = self.client.post(
            self.proposals_url,
            data={
                "name": "O obrotach sfer niebieskich",
                "duration_minutes": 600,
                "city": "Toruń",
                "club": "A",
                "phone": "+4812",
                "needs": "no",
                "waitlist": self.wait_list.id,
                "time_slots": [t_s.id for t_s in self.time_slots],
                "speaker_user": str(self.user.uuid),
                "topic": "Literature",
            },
        )
        res_data = res.json()
        proposal = Proposal.objects.first()
        assert proposal.city == res_data.pop("city") == "Toruń"
        assert proposal.club == res_data.pop("club") == "A"
        assert proposal.description == res_data.pop("description") == ""
        assert proposal.duration_minutes == res_data.pop("duration_minutes") == 600
        assert proposal.id == res_data.pop("id") == 1
        assert proposal.meeting == res_data.pop("meeting") == None
        assert proposal.name == res_data.pop("name") == "O obrotach sfer niebieskich"
        assert proposal.needs == res_data.pop("needs") == "no"
        assert proposal.other_contact == res_data.pop("other_contact") == {}
        assert proposal.other_data == res_data.pop("other_data") == {}
        assert proposal.phone == res_data.pop("phone") == "+4812"
        assert (
            proposal.speaker_name
            == res_data.pop("speaker_name")
            == "Mszczuj ze Skzynna"
        )
        assert (
            str(proposal.speaker_user.uuid)
            == res_data.pop("speaker_user")
            == str(self.user.uuid)
        )
        assert proposal.status == res_data.pop("status") == "CREATED"
        assert (
            list(proposal.time_slots.values_list("id", flat=True))
            == res_data.pop("time_slots")
            == [1, 2]
        )
        assert proposal.topic == res_data.pop("topic") == "Literature"
        assert proposal.waitlist.id == res_data.pop("waitlist") == 1
        self.assertEqual(res_data, {})

    @freeze_time("2020-07-04")
    def test_create_no_user(self):
        res = self.client.post(
            self.proposals_url,
            data={
                "name": "O obrotach sfer niebieskich",
                "duration_minutes": 600,
                "city": "Toruń",
                "club": "A",
                "phone": "+4812",
                "needs": "no",
                "waitlist": self.wait_list.id,
                "time_slots": [t_s.id for t_s in self.time_slots],
                "speaker_name": "Mr Mszczuj",
                "topic": "Literature",
            },
        )
        res_data = res.json()
        proposal = Proposal.objects.first()
        assert proposal.city == res_data.pop("city") == "Toruń"
        assert proposal.club == res_data.pop("club") == "A"
        assert proposal.description == res_data.pop("description") == ""
        assert proposal.duration_minutes == res_data.pop("duration_minutes") == 600
        assert proposal.id == res_data.pop("id") == 1
        assert proposal.meeting == res_data.pop("meeting") == None
        assert proposal.name == res_data.pop("name") == "O obrotach sfer niebieskich"
        assert proposal.needs == res_data.pop("needs") == "no"
        assert proposal.other_contact == res_data.pop("other_contact") == {}
        assert proposal.other_data == res_data.pop("other_data") == {}
        assert proposal.phone == res_data.pop("phone") == "+4812"
        assert proposal.speaker_name == res_data.pop("speaker_name") == "Mr Mszczuj"
        assert proposal.speaker_user == res_data.pop("speaker_user") == None
        assert proposal.status == res_data.pop("status") == "CREATED"
        assert (
            list(proposal.time_slots.values_list("id", flat=True))
            == res_data.pop("time_slots")
            == [1, 2]
        )
        assert proposal.topic == res_data.pop("topic") == "Literature"
        assert proposal.waitlist.id == res_data.pop("waitlist") == 1
        self.assertEqual(res_data, {})

    @freeze_time("2020-07-04")
    def test_create_no_user_data_error(self):
        res = self.client.post(
            self.proposals_url,
            data={
                "name": "O obrotach sfer niebieskich",
                "duration_minutes": 600,
                "city": "Toruń",
                "club": "A",
                "phone": "+4812",
                "needs": "no",
                "waitlist": self.wait_list.id,
                "time_slots": [t_s.id for t_s in self.time_slots],
            },
        )
        res_data = res.json()
        self.assertEqual(
            res_data["non_field_errors"], ["No speaker name nor speaker user"]
        )

    @freeze_time("2020-07-04")
    def test_update(self):
        proposal = ProposalFactory(
            name="Lightning talk", speaker_name="B. Franklin", waitlist=self.wait_list
        )
        res = self.client.patch(
            reverse("v1:chronology:proposals-detail", kwargs={"id": proposal.id}),
            data={"speaker_name": "N. Tesla"},
        )
        res_data = res.json()
        proposal.refresh_from_db()
        self.assertEqual(proposal.speaker_name, "N. Tesla")
        self.assertEqual(res_data.get("speaker_name"), "N. Tesla")
