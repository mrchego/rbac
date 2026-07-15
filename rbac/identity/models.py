from django.db import models
from django.utils import timezone
from rbac.core.models.base import BaseModel


class VerificationCode(BaseModel):
    class Purpose(models.TextChoices):
        EMAIL_VERIFICATION = "EMAIL_VERIFICATION", "Email Verification"
        PASSWORD_RESET = "PASSWORD_RESET", "Password Reset"

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="verification_codes"
    )
    purpose = models.CharField(max_length=30, choices=Purpose.choices)
    code = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "purpose", "used_at"]),
        ]

    @property
    def is_expired(self) -> bool:
        return timezone.now() >= self.expires_at

    @property
    def is_used(self) -> bool:
        return self.used_at is not None

    def __str__(self):
        return f"{self.purpose} code for {self.user.email}"