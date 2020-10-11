from typing import List

from django.urls.resolvers import URLPattern
from rest_framework import routers

from .views import ProposalAPIView

router: routers.SimpleRouter = routers.SimpleRouter()

router.register("proposals", ProposalAPIView, basename="proposals")

urlpatterns: List[URLPattern] = router.urls
