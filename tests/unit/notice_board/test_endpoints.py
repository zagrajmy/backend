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
        self.meeting_1 = MeetingFactory(participants_limit=2)
        self.meeting_2 = MeetingFactory(participants_limit=4)
        self.meeting_3 = MeetingFactory(participants_limit=-1)
        self.meeting_4 = MeetingFactory(participants_limit=0)
        self.meeting_5 = MeetingFactory(participants_limit=None)
        for _ in range(4):
            MeetingParticipant.objects.create(
                user=UserFactory(),
                meeting=self.meeting_2,
                status=MeetingParticipant.CONFIRMED,
            )
        self.add_participant_url = reverse(
            "v1:notice_board:meeting-add-participant",
            kwargs={"pk": self.meeting_1.pk},
        )
        self.client.force_authenticate(user=self.user)  # pylint: disable=no-member

    def test_add_participant(self):
        res = self.client.post(
            self.add_participant_url,
            data={},
        )
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

    def test_add_participant_unlimited_meeting(self):
        res = self.client.post(
            reverse(
                "v1:notice_board:meeting-add-participant",
                kwargs={"pk": self.meeting_3.pk},
            ),
            data={},
        )
        participant = MeetingParticipant.objects.get(
            meeting=self.meeting_3, user=self.user
        )
        self.assertEqual(participant.status, MeetingParticipant.CONFIRMED)
        self.assertEqual(res.json().get("status"), MeetingParticipant.CONFIRMED.lower())

    def test_trying_add_participant_not_applicable_none(self):
        res = self.client.post(
            reverse(
                "v1:notice_board:meeting-add-participant",
                kwargs={"pk": self.meeting_4.pk},
            ),
            data={},
        )
        participants = MeetingParticipant.objects.filter(
            meeting=self.meeting_4, user=self.user
        )
        self.assertEqual(len(participants), 0)
        self.assertEqual(res.json().get("status"), None)

    def test_trying_add_participant_not_applicable_zero(self):
        res = self.client.post(
            reverse(
                "v1:notice_board:meeting-add-participant",
                kwargs={"pk": self.meeting_4.pk},
            ),
            data={},
        )
        participants = MeetingParticipant.objects.filter(
            meeting=self.meeting_4, user=self.user
        )
        self.assertEqual(len(participants), 0)
        self.assertEqual(res.json().get("status"), None)

    def test_remove_participant(self):
        meeting = MeetingFactory()
        MeetingParticipant.objects.create(
            user=self.user,
            meeting=meeting,
            status=MeetingParticipant.CONFIRMED,
        )
        self.client.force_authenticate(user=self.user)  # pylint: disable=no-member
        remove_participant_url = reverse(
            "v1:notice_board:meeting-remove-participant",
            kwargs={"pk": meeting.pk},
        )
        res = self.client.post(
            remove_participant_url,
            data={},
        )
        self.assertAlmostEqual(res.json(), {"status": "OK"})
        meeting.refresh_from_db()
        self.assertEqual(len(meeting.participants.all()), 0)
