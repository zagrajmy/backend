from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NoticeBoardConfig(AppConfig):
    """Notice Board application config."""

    name = "notice_board"
    verbose_name = _("notice board")
