from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from rbac.accounts.managers import UserManager
from rbac.core.models.mixins import TimeStampedMixin, UUIDMixin
from rbac.core.utils.files import avatar_upload_path
from rbac.core.validators.phone import validate_phone_number


class User(UUIDMixin, TimeStampedMixin, AbstractUser):
    """
    Custom user model.

    Responsible for:
    - Authentication
    - Basic identity
    - Basic profile

    Employment-specific information belongs in the future Staff app.
    """

    username = None
    name = None

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------
    email = models.EmailField(_("Email Address"), unique=True)

    is_email_verified = models.BooleanField(
        default=False,
        help_text=_("Whether the user has confirmed ownership of their email address."),
    )

    first_name = models.CharField(
        _("First Name"),
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        _("Last Name"),
        max_length=100,
        blank=True,
    )

    phone = models.CharField(
        _("Phone Number"),
        max_length=20,
        blank=True,
        validators=[validate_phone_number],
    )

    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True,
        null=True,
    )
    
    is_founder = models.BooleanField(
        default=False,
        help_text=_(
            "The user who originally registered the company. Founders cannot be "
            "deactivated, locked, deleted, or demoted from ownership by anyone, "
            "including other owners."
        ),
    )

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------
    company = models.ForeignKey(
        "company.Company",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    can_login = models.BooleanField(
        default=True,
        help_text=_("Determines whether the user can sign in."),
    )

    password_reset_required = models.BooleanField(default=False)

    last_password_change = models.DateTimeField(
        null=True,
        blank=True,
    )

    failed_login_attempts = models.PositiveIntegerField(default=0)

    locked_until = models.DateTimeField(
        null=True,
        blank=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["can_login"]),
        ]

    @property
    def full_name(self) -> str:
        """
        Returns the user's full name.

        Examples:
            John Doe
            John
            Doe
            ""
        """
        return " ".join(part for part in [self.first_name, self.last_name] if part)

    @property
    def display_name(self) -> str:
        """
        Returns the best available display name.
        """
        return self.full_name or self.email

    @property
    def is_locked(self) -> bool:
        """
        Indicates whether the account is currently locked.
        """
        from django.utils import timezone

        return self.locked_until is not None and self.locked_until > timezone.now()

    def __str__(self) -> str:
        return self.display_name
