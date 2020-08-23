from django.urls import include, path

urlpatterns = [
    path("crowd/", include(("crowd.urls_v1", "crowd"), namespace="crowd")),
    path(
        "chronology/", include(("chronology.urls_v1", "crowd"), namespace="chronology")
    ),
    path(
        "notice_board/",
        include(("notice_board.urls_v1", "notice_board"), namespace="notice_board"),
    ),
]
