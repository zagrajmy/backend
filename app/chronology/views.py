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

    queryset = Proposal.objects.all()
    serializer_class: Type[ProposalSerializer] = ProposalSerializer
    lookup_url_kwarg: str = "id"
