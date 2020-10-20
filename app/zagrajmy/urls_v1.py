from django.urls import include, path
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path("crowd/", include(("crowd.urls_v1", "crowd"), namespace="crowd")),
    path(
        "chronology/",
        include(("chronology.urls_v1", "chronology"), namespace="chronology"),
    ),
    path(
        "notice_board/",
        include(("notice_board.urls_v1", "notice_board"), namespace="notice_board"),
    ),
    path(
        "openapi",
        get_schema_view(title="Zagrajmy", version="1.0.0"),
        name="openapi-schema",
    ),
    path("social/", include("dj_rest_auth.urls")),
    path("social/registration/", include("dj_rest_auth.registration.urls")),
]
