from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from chronology.models import Proposal
from chronology.serializers import ProposalSerializer


class ProposalAPIView(CreateModelMixin, UpdateModelMixin, GenericViewSet):

    serializer_class = ProposalSerializer
    lookup_url_kwarg = "id"

    def get_queryset(self):
        return Proposal.objects.all()

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
