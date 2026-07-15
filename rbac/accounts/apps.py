from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rbac.accounts"
    label = "accounts"
    verbose_name = _("Accounts")

    def ready(self):
        # Import signals here later if needed (e.g., send email on password reset)
        pass