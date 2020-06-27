# """
# behave environment module for testing behave-django
# """
from django.core.management import call_command


def before_all(context):
    context.fixtures = ["app/contrib/auth/fixtures/sphere-manager.json"]


def django_ready(context):
    context.django = True
