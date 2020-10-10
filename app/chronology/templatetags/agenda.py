from datetime import datetime
from typing import Optional, TypedDict

import pytz
from django import template
from django.template.loader import render_to_string
from django.urls import reverse

from ..admin import URL_HOUR_FORMAT
from ..models import AgendaItem, Room

register = template.Library()


class AgendaCellContext(TypedDict):
    add_related_url: str
    can_add_related: bool
    can_change_related: bool
    can_delete_related: bool
    change_related_template_url: str
    delete_related_template_url: str
    is_hidden: bool
    model: Optional[str]
    name: str
    url_params: str
    rendered_widget: str


def _get_modify_link(action: str) -> str:
    return reverse(f"admin:chronology_agendaitem_{action}", args=("__fk__",))


@register.inclusion_tag("admin/widgets/related_widget_wrapper.html")
def agenda_cell(  # type:ignore[misc]
    room: Room, hour: datetime, agenda_item: Optional[AgendaItem] = None
) -> AgendaCellContext:
    formatted_hour = hour.astimezone(pytz.UTC).strftime(URL_HOUR_FORMAT)
    return {
        "add_related_url": reverse("admin:chronology_agendaitem_add"),
        "can_add_related": True,
        "can_change_related": True,
        "can_delete_related": True,
        "change_related_template_url": _get_modify_link("change"),
        "delete_related_template_url": _get_modify_link("delete"),
        "is_hidden": False,
        "model": AgendaItem._meta.verbose_name,
        "name": f"agendaitem_r{room.id}_t{formatted_hour}",
        "url_params": f"_to_field=id&_popup=1&room={room.id}&hour={formatted_hour}",
        "rendered_widget": render_to_string(
            "chronology/agenda_item.html",
            {
                "agenda_item": agenda_item,
                "name": f"agendaitem_r{room.id}_t{formatted_hour}",
            },
        ),
    }
