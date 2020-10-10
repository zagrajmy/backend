"""Zagrajmy root url config."""

from typing import List, Union

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

urlpatterns: List[Union[URLPattern, URLResolver]] = [
    path("admin/", admin.site.urls),
    path("v1/", include(("zagrajmy.urls_v1", "v1"), namespace="v1")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
