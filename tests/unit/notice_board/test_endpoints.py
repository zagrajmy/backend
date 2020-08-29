from django.urls import reverse
from rest_framework.test import APITestCase

from crowd.models import User
from notice_board.models import MeetingParticipant
from tests.factories import MeetingFactory, UserFactory


class TestProposals(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            first_name="Mszczuj", last_name="ze Skzynna", username="PanMszczuj"
        )
        self.meeting_1 = MeetingFactory()
        self.meeting_2 = MeetingFactory(participants_limit=4)
        for _ in range(4):
            MeetingParticipant.objects.create(
                user=UserFactory(),
                meeting=self.meeting_2,
                status=MeetingParticipant.CONFIRMED,
            )
        self.add_participant_url = reverse(
            "v1:notice_board:meeting-add-participant", kwargs={"pk": self.meeting_1.pk},
        )
        self.client.force_authenticate(user=self.user)  # pylint: disable=no-member

    def test_add_participant(self):
        res = self.client.post(self.add_participant_url, data={},)
        participant = MeetingParticipant.objects.get(
            meeting=self.meeting_1, user=self.user
        )
        self.assertEqual(participant.status, MeetingParticipant.CONFIRMED)
        self.assertEqual(res.json().get("status"), MeetingParticipant.CONFIRMED.lower())

    def test_add_participant_full_meeting(self):
        res = self.client.post(
            reverse(
                "v1:notice_board:meeting-add-participant",
                kwargs={"pk": self.meeting_2.pk},
            ),
            data={},
        )
        participant = MeetingParticipant.objects.get(
            meeting=self.meeting_2, user=self.user
        )
        self.assertEqual(participant.status, MeetingParticipant.WAITING)
        self.assertEqual(res.json().get("status"), MeetingParticipant.WAITING.lower())
