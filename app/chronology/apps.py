from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ChronologyConfig(AppConfig):
    name = "chronology"
    verbose_name = _("Chronology")
