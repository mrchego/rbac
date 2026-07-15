from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AuthorizationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rbac.authorization"
    label = "authorization"
    verbose_name = _("Authorization")

    def ready(self):
        # Import signals here later if needed (e.g., send email on password reset)
        pass
 