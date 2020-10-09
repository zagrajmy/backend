# pylint: disable=unused-wildcard-import
from .base import *  # pylint: disable=wildcard-import

DEBUG = True

INSTALLED_APPS += [
    "behave_django",
    "django_extensions",
]


INTERNAL_IPS = [
    "127.0.0.1",
]
