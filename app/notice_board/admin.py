"""Django admin customizations."""

from typing import Tuple

from django.contrib import admin
from django.db.models import QuerySet  # pylint: disable=unused-import
from django.http import HttpRequest
from notice_board.models import Guild, Meeting, Sphere


class SphereManagersAdmin(admin.ModelAdmin):
    """Limits queryset by sphere manager."""

    permission_keys = {
        "AgendaItem": "room__festival__sphere__managers",
        "Festival": "sphere__managers",
        "Helper": "festival__sphere__managers",
        "Meeting": "sphere__managers",
        "Room": "festival__sphere__managers",
        "Sphere": "managers",
        "TimeSlot": "festival__sphere__managers",
        "WaitList": "festival__sphere__managers",
        "Proposal": "waitlist__festival__sphere__managers",
    }

    def get_list_display(self, request: HttpRequest) -> Tuple[str]:
        list_display = super().get_list_display(request)
        return tuple(["id"] + list(list_display))

    def get_list_display_links(
        self, request: HttpRequest, list_display: Tuple[str]
    ) -> str:
        return list_display[1]

    def get_queryset(self, request: HttpRequest) -> "QuerySet[...]":
        """Limit querset to show only spheres that user is managing."""
        queryset = super().get_queryset(request)

        return self._get_queryset(request.user, queryset, self.model.__name__)

    def get_field_queryset(self, db, db_field, request: HttpRequest) -> "QuerySet[...]":
        queryset = super().get_field_queryset(db, db_field, request)

        if queryset is None:
            queryset = db_field.remote_field.model.objects.all()

        return self._get_queryset(
            request.user, queryset, db_field.remote_field.model.__name__
        )

    def _get_queryset(self, user, queryset, model_name):
        if not user.is_superuser:
            key = self.permission_keys[model_name]
            if key:
                return queryset.filter(**{key: user})
        return queryset


admin.site.register(Guild)
admin.site.register(Sphere, SphereManagersAdmin)
admin.site.register(Meeting, SphereManagersAdmin)
