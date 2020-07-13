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
            first_name="Mszczuj",
            last_name="ze Skzynna",
            username="PanMszczuj"
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
                "contact_info": "poczta",
                "phone": "+4812",
                "needs": "no",
                "waitlist": self.wait_list.id,
                "time_slots": [t_s.id for t_s in self.time_slots],
                "speaker_user": str(self.user.uuid),
            },
        )
        res_data = res.json()
        proposal = Proposal.objects.first()
        self.assertEqual(proposal.name, "O obrotach sfer niebieskich")
        self.assertEqual(res_data.get("name"), "O obrotach sfer niebieskich")
        self.assertEqual(proposal.duration_minutes, 600)
        self.assertEqual(res_data.get("duration_minutes"), 600)
        self.assertEqual(proposal.city, "Toruń")
        self.assertEqual(res_data.get("city"), "Toruń")
        self.assertEqual(proposal.club, "A")
        self.assertEqual(res_data.get("club"), "A")
        self.assertEqual(proposal.contact_info, "poczta")
        self.assertEqual(res_data.get("contact_info"), "poczta")
        self.assertEqual(proposal.phone, "+4812")
        self.assertEqual(res_data.get("phone"), "+4812")
        self.assertEqual(proposal.speaker_name, "Mszczuj ze Skzynna")
        self.assertEqual(res_data.get("speaker_name"), "Mszczuj ze Skzynna")

    @freeze_time("2020-07-04")
    def test_create_no_user(self):
        res = self.client.post(
            self.proposals_url,
            data={
                "name": "O obrotach sfer niebieskich",
                "duration_minutes": 600,
                "city": "Toruń",
                "club": "A",
                "contact_info": "poczta",
                "phone": "+4812",
                "needs": "no",
                "waitlist": self.wait_list.id,
                "time_slots": [t_s.id for t_s in self.time_slots],
                "speaker_name": "Mr Mszczuj"
            },
        )
        res_data = res.json()
        proposal = Proposal.objects.first()
        self.assertEqual(proposal.name, "O obrotach sfer niebieskich")
        self.assertEqual(res_data.get("name"), "O obrotach sfer niebieskich")
        self.assertEqual(proposal.duration_minutes, 600)
        self.assertEqual(res_data.get("duration_minutes"), 600)
        self.assertEqual(proposal.city, "Toruń")
        self.assertEqual(res_data.get("city"), "Toruń")
        self.assertEqual(proposal.club, "A")
        self.assertEqual(res_data.get("club"), "A")
        self.assertEqual(proposal.contact_info, "poczta")
        self.assertEqual(res_data.get("contact_info"), "poczta")
        self.assertEqual(proposal.phone, "+4812")
        self.assertEqual(res_data.get("phone"), "+4812")
        self.assertEqual(proposal.speaker_name, "Mr Mszczuj")
        self.assertEqual(res_data.get("speaker_name"), "Mr Mszczuj")

    @freeze_time("2020-07-04")
    def test_create_no_user_data_error(self):
        res = self.client.post(
            self.proposals_url,
            data={
                "name": "O obrotach sfer niebieskich",
                "duration_minutes": 600,
                "city": "Toruń",
                "club": "A",
                "contact_info": "pidgeon mail accepted",
                "phone": "+4812",
                "needs": "no",
                "waitlist": self.wait_list.id,
                "time_slots": [t_s.id for t_s in self.time_slots]
            },
        )
        res_data = res.json()
        self.assertEqual(
            res_data["non_field_errors"],
            ['No speaker name nor speaker user']
        )

    @freeze_time("2020-07-04")
    def test_update(self):
        proposal = ProposalFactory(
            name="Lightning talk",
            speaker_name="B. Franklin",
            waitlist=self.wait_list
        )
        res = self.client.patch(
            reverse(
                "v1:chronology:proposals-detail",
                kwargs={"id": proposal.id}
            ),
            data={
                "speaker_name": "N. Tesla"
            },
        )
        res_data = res.json()
        proposal.refresh_from_db()
        self.assertEqual(proposal.speaker_name, "N. Tesla")
        self.assertEqual(res_data.get("speaker_name"), "N. Tesla")
