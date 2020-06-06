from rest_framework import response, status, viewsets

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_url_kwarg = "uuid"
    lookup_field = "uuid"
