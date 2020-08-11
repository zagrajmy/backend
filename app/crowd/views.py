from typing import Type

from django.db.models import QuerySet  # pylint: disable=unused-import
from rest_framework import viewsets

from crowd.models import User
from crowd.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset: "QuerySet[User]" = User.objects.all()
    serializer_class: Type[UserSerializer] = UserSerializer
    lookup_url_kwarg: str = "uuid"
    lookup_field: str = "uuid"
