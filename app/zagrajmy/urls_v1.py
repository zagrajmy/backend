from django.urls import include, path
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("crowd/", include(("crowd.urls_v1", "crowd"), namespace="crowd")),
    path(
        "chronology/", include(("chronology.urls_v1", "crowd"), namespace="chronology")
    ),
    path(
        "openapi",
        get_schema_view(title="Zagrajmy", version="1.0.0"),
        name="openapi-schema",
    ),
]
