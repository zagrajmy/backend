import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):  # type: ignore[misc]
    """Zagrajmy user model."""

    auth0_id = models.CharField(
        blank=True, default="", max_length=255, verbose_name=_("auth0 id")
    )
    locale = models.CharField(max_length=20, default="en", verbose_name=_("locale"))
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("uuid")
    )

    class Meta:  # noqa: D106
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "cr_user"
        constraints = [
            models.UniqueConstraint(
                fields=["auth0_id"],
                condition=~models.Q(auth0_id=""),
                name="unique_nonempty_auth0_id",
            )
        ]

    def __str__(self) -> str:
        return self.get_full_name() or self.username
