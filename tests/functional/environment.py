# """
# behave environment module for testing behave-django
# """
from rest_framework.test import APIClient


def before_all(context):
    context.fixtures = ["app/contrib/auth/fixtures/sphere-manager.json"]
    context.api_client = APIClient()


def after_scenario(context, scenario):
    del scenario

    context.api_client.logout()


def django_ready(context):
    context.django = True
