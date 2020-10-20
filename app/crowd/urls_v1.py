from typing import List
from django.urls import path
from django.urls.resolvers import URLPattern
from rest_framework import routers

from .views import UserViewSet, GoogleLogin, FacebookLogin

router = routers.SimpleRouter()

router.register("users", UserViewSet, basename="users")

urlpatterns: List[URLPattern] = router.urls

urlpatterns += [
    path("social/google/", GoogleLogin.as_view(), name="google_login"),
    path("social/facebook/", FacebookLogin.as_view(), name="facebook_login"),
]
