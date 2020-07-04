from rest_framework import viewsets

from crowd.models import User
from crowd.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "uuid"
    lookup_field = "uuid"
