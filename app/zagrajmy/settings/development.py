# pylint: disable=unused-wildcard-import
from zagrajmy.settings.base import *  # pylint: disable=wildcard-import
import os

DEBUG = True

INSTALLED_APPS += [
    "behave_django",
    "django_extensions",
]


INTERNAL_IPS = [
    "127.0.0.1",
]

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(" ")
