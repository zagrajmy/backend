from collections import defaultdict
from random import random

from behave import given, then, when  # pylint: disable=no-name-in-module
from django.contrib.auth.models import Group
from django.urls import reverse
from lxml import html

from crowd.models import User
from tests.factories import FACTORIES


@given("a set of staff users")
def __(context):
    sphere_manager_group = Group.objects.get(name="Sphere Manager")
    context.users = {}

    for row in context.table:
        password = str(random())
        user = User.objects.create(username=row["username"], is_staff=True,)
        user.set_password(password)
        user.groups.add(sphere_manager_group)
        user.save()
        context.users[user.username] = user, password


SPHERE_ARG = {
    "agendaitem": "room__festival__sphere",
    "festival": "sphere",
    "helper": "festival__sphere",
    "meeting": "sphere",
    "proposal": "waitlist__festival__sphere",
    "room": "festival__sphere",
    "timeslot": "festival__sphere",
    "waitlist": "festival__sphere",
}


@given("'{name}' instance of {model} connected to {user}'s sphere")
def __(context, name, model, user):
    sphere = FACTORIES["sphere"].create()
    sphere.managers.set([context.users[user][0]])

    if not hasattr(context, "instances"):
        context.instances = {}

    if model == "sphere":
        context.instances[name] = sphere
    else:
        arg = SPHERE_ARG[model]
        context.instances[name] = FACTORIES[model].create(**{arg: sphere})


@given("{username} is logged in")
def __(context, username):
    assert context.test.client.login(
        username=username, password=context.users[username][1]
    )


XPATH = {
    "changelist": (
        '//form[@id="changelist-form"]/div/table/tbody/tr/'
        'th[@class="field-id"]/a[text()="{}"]'
    )
}


@then("I can see only '{instance1}', not '{instance2}'")
def __(context, instance1, instance2):
    for action, response in context.responses:
        tree = html.fromstring(response.content)
        assert tree.xpath(
            XPATH[action].format(context.instances[instance1].pk)
        ), "Can't see my instance"
        assert not tree.xpath(
            XPATH[action].format(context.instances[instance2].pk)
        ), "Shouldn't see not mine instance"


@then("He can access only '{instance1}', not '{instance2}'")
def __(context, instance1, instance2):
    for response in context.responses[instance1]:
        assert response.status_code == 200
    for response in context.responses[instance2]:
        assert response.status_code == 302
        assert response["Location"] == "/admin/"


@then("The result is error code {status}")
def __(context, status):
    for __, response in context.responses:
        assert response.status_code == int(status), response.status_code


@given("there is any {model}")
def __(context, model):
    context.model_obj = FACTORIES[model].create()


PAGES = {
    "create": [("add", "get", True), ("add", "post", True)],
    "delete": [
        ("changelist", "post", False),
        ("delete", "post", True),
        ("delete", "get", True),
    ],
    "list": [("changelist", "get", False)],
    "read": [("change", "get", True)],
    "update": [("change", "post", True)],
}


@when("User tries {action} on model {model} in app {app}")
def __(context, action, model, app):
    pages = PAGES[action]
    args = [context.model_obj.pk] if hasattr(context, "model_obj") else []
    context.responses = []
    for admin_action, method, needs_args in pages:
        response = getattr(context.test.client, method)(
            reverse(
                f"admin:{app}_{model}_{admin_action}", args=args if needs_args else []
            )
        )
        context.responses.append((admin_action, response))


@when("User tries {action} on instance '{instance}' of model {model} in app {app}")
def __(context, action, instance, model, app):
    pages = PAGES[action]
    if not hasattr(context, "responses"):
        context.responses = defaultdict(list)
    for admin_action, method, __ in pages:
        response = getattr(context.test.client, method)(
            reverse(
                f"admin:{app}_{model}_{admin_action}",
                args=[context.instances[instance].pk],
            )
        )
        context.responses[instance].append(response)
