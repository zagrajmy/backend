from rest_framework import routers

from chronology.views import ProposalAPIView

router = routers.SimpleRouter()

router.register("proposals", ProposalAPIView, basename="proposals")

urlpatterns = router.urls
