# """
# With these settings, tests run faster.
# """

# from .base import *  # noqa: F403
# from .base import TEMPLATES
# from .base import env

# # GENERAL
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# SECRET_KEY = env(
#     "DJANGO_SECRET_KEY",
#     default="d2dCHzXdMIpF3Y84wNB9KQLMBHEkFhvaQAQMKdv4C5n85Z4j1k8XLbDGeqTpChgC",
# )
# # https://docs.djangoproject.com/en/dev/ref/settings/#test-runner
# TEST_RUNNER = "django.test.runner.DiscoverRunner"

# # PASSWORDS
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
# PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

# # EMAIL
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# # DEBUGGING FOR TEMPLATES
# # ------------------------------------------------------------------------------
# TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore[index]

# # MEDIA
# # ------------------------------------------------------------------------------
# # https://docs.djangoproject.com/en/dev/ref/settings/#media-url
# MEDIA_URL = "http://media.testserver/"
# # Your stuff...
# # ------------------------------------------------------------------------------
import os

os.environ.setdefault('DATABASE_URL', 'sqlite:///:memory:')

from .base import *  # noqa: F403

SECRET_KEY = "django-insecure-test-key"
DEBUG = False
TEMPLATE_DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# ---------- CACHES: use a dummy cache to avoid table creation ----------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"