from typing import List

from django.urls.resolvers import URLPattern
from rest_framework import routers

from crowd.views import UserViewSet

router = routers.SimpleRouter()

router.register("users", UserViewSet, basename="users")

urlpatterns: List[URLPattern] = router.urls
