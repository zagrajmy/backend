# pylint: disable=unused-wildcard-import
from .base import *  # pylint: disable=wildcard-import

DEBUG = True

INSTALLED_APPS += ["behave_django"]

DATABASES["default"]["NAME"] = ":memory:"
