from django.urls import include, path

urlpatterns = [
    path("crowd/", include(("crowd.urls_v1", "crowd"), namespace="crowd")),
]
