from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CrowdConfig(AppConfig):
    """User management app config."""

    name = "crowd"
    verbose_name = _("crowd")
