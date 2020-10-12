from __future__ import annotations

from typing import Type

from django.db.models import QuerySet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Proposal
from .serializers import ProposalSerializer


class ProposalAPIView(CreateModelMixin, UpdateModelMixin, GenericViewSet):

    serializer_class: Type[ProposalSerializer] = ProposalSerializer
    lookup_url_kwarg: str = "id"

    def get_queryset(self) -> QuerySet[Proposal]:
        return Proposal.objects.all()

    def put(self, request: Request, partial: bool = False) -> Response:
        return self.update(request, partial=partial)

    def patch(self, request: Request, partial: bool = True) -> Response:
        return self.partial_update(request, partial=partial)
