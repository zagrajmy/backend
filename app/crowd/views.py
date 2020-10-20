from __future__ import annotations

from typing import Type

from django.db.models import QuerySet
from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter


class UserViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[User] = User.objects.all()
    serializer_class: Type[UserSerializer] = UserSerializer
    lookup_url_kwarg: str = "uuid"
    lookup_field: str = "uuid"


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
