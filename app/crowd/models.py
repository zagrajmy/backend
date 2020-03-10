import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Zagrajmy user model."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:  # noqa: D106
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "cr_user"
