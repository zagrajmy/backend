from __future__ import annotations

from typing import Optional, Type

from django.db.models import QuerySet  # pylint: disable=unused-import
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Meeting, MeetingParticipant
from .serializers import (
    MeetingCreateSerializer,
    MeetingReadSerializer,
    MeetingUpdateSerializer,
)


class MeetingViewSet(
    CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    queryset: QuerySet[Meeting] = Meeting.objects.all()
    serializer_classes = {
        "create": MeetingCreateSerializer,
        "update": MeetingUpdateSerializer,
    }
    serializer_class: Type[MeetingReadSerializer] = MeetingReadSerializer
    lookup_url_kwarg: str = "pk"
    lookup_field: str = "pk"

    def get_serializer_class(self) -> Type[serializers.BaseSerializer]:
        return self.serializer_classes.get(self.action, super().get_serializer_class())

    # pylint: disable=unused-argument
    @action(detail=True, methods=["post"])
    def add_participant(self, request: Request, pk: Optional[int] = None) -> Response:
        meeting = self.get_object()
        if meeting.participants_limit is None or meeting.participants_limit == 0:
            return Response({"status": None})
        if meeting.participants_limit < 0:
            meeting.participants.add(
                request.user, through_defaults={"status": MeetingParticipant.CONFIRMED}
            )
            return Response({"status": "confirmed"})
        MeetingParticipant.objects.create(
            meeting=meeting,
            user=request.user,
            status=MeetingParticipant.WAITING,
        )
        status = MeetingParticipant.WAITING
        participants = MeetingParticipant.objects.filter(
            meeting=meeting,
        ).order_by("created_at")
        for i, participant in enumerate(participants):
            if i >= meeting.participants_limit:
                break
            if participant.user == request.user:
                participant.status = MeetingParticipant.CONFIRMED
                status = participant.status
                participant.save()
        return Response({"status": status.lower()})

    # pylint: disable=unused-argument
    @action(detail=True, methods=["post"])
    def remove_participant(
        self, request: Request, pk: Optional[int] = None
    ) -> Response:
        meeting = self.get_object()
        meeting.participants.remove(request.user)
        return Response({"status": "OK"})
