from typing import List

from django.urls.resolvers import URLPattern
from rest_framework import routers

from .viewsets import MeetingViewSet

router = routers.SimpleRouter()

router.register("meetings", MeetingViewSet, basename="meetings")

urlpatterns: List[URLPattern] = router.urls
