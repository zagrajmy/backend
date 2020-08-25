from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from notice_board.models import Meeting, Participant
from notice_board.serializers import MeetingSerializer


class MeetingViewSet(ModelViewSet):

    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

    @action(detail=True, methods=["post"])
    def add_participant(self, request: Request, pk=None):
        meeting = self.get_object()
        if meeting.participants_limit < 1:
            meeting.participants.add(
                request.user, through_defaults={"status": Participant.CONFIRMED}
            )
            return Response({"status": "confirmed"})
        Participant.objects.create(
            meeting=meeting, user=request.user, status=Participant.WAITING,
        )
        status = Participant.WAITING
        participants = Participant.objects.filter(meeting=meeting,).order_by(
            "created_at"
        )
        for i, participant in enumerate(participants):
            if i >= meeting.participants_limit:
                break
            if participant.user == request.user:
                participant.status = Participant.CONFIRMED
                status = participant.status
                participant.save()
        return Response({"status": status.lower()})
