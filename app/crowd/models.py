import uuid
from typing import Any, Optional

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CrowdUserManager(UserManager):  # type: ignore
    """Manager allowing username OR first_name as required argument."""

    def create_user(
        self,
        username: str = "",
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> AbstractUser:
        """Create user requiring username or first_name."""
        return super().create_user(  # type: ignore
            username, email, password, **extra_fields
        )

    def _create_user(
        self,
        username: str = "",
        email: Optional[str] = None,
        password: Optional[str] = None,
        **extra_fields: Any,
    ) -> AbstractUser:
        """Create and save a user with the given username, email, and password."""
        if not username and not extra_fields.get("first_name"):
            raise ValidationError("Missing username or first_name.")
        email = self.normalize_email(email)
        username = self.model.normalize_username(username) if username else ""
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # type: ignore
        return user  # type: ignore


class User(AbstractUser):
    """Zagrajmy user model."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(_("username"), max_length=255, blank=True)

    USERNAME_FIELD = "uuid"

    objects = CrowdUserManager()

    class Meta:  # noqa: D106
        verbose_name = _("user")
        verbose_name_plural = _("users")
        db_table = "cr_user"

    def __str__(self) -> str:
        """Use username or full name as string representation."""
        return self.get_full_name()

    def get_full_name(self) -> str:
        """Return the first_name plus the last_name, with a username in between."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        if self.username:
            full_name = f"{full_name} ({self.username})"
        return full_name

    def clean(self) -> None:
        """Model-wide validation."""
        super().clean()
        if not self.username and not self.first_name:
            raise ValidationError("Missing username or first_name.")
