from typing import List

from django.urls.resolvers import URLPattern
from rest_framework import routers

from notice_board.views import MeetingViewSet

router = routers.SimpleRouter()

router.register("meeting", MeetingViewSet, basename="meeting")

urlpatterns: List[URLPattern] = router.urls
