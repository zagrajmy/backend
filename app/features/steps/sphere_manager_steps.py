from behave import given, step, then, when
from crowd.models import User
from django.contrib.auth.models import Group
from django.urls import reverse
from notice_board.models import Sphere
from random import random
from factories import FACTORIES
from lxml import html
from chronology.models import Room


@given("a set of staff users")
def step_impl(context):
    sphere_manager_group = Group.objects.get(name="Sphere Manager")
    context.users = {}

    for row in context.table:
        password = str(random())
        user = User.objects.create(username=row["username"], is_staff=True,)
        user.set_password(password)
        user.groups.add(sphere_manager_group)
        user.save()
        context.users[user.username] = user, password


@given("a set of spheres")
def step_impl(context):
    context.spheres = {}

    for row in context.table:
        sphere = Sphere.objects.create(name=row["name"])
        sphere.managers.add(context.users[row["managers"]][0])
        context.spheres["sphere.name"] = sphere


SPHERE_ARG = {
    "agendaitem": "room__festival__sphere",
    "festival": "sphere",
    "helper": "festival__sphere",
    "proposal": "waitlist__festival__sphere",
    "room": "festival__sphere",
    "timeslot": "festival__sphere",
    "waitlist": "festival__sphere",
}


@given("'{name}' instance of {model} connected to {user}'s sphere")
def step_impl(context, name, model, user):
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
def step_impl(context, username):
    assert context.test.client.login(
        username=username, password=context.users[username][1]
    )


XPATH = {
    "changelist": (
        '//form[@id="changelist-form"]/div/table/tbody/tr/'
        'td[@class="field-id"][text()="{}"]'
    )
}


@then("I can see only '{instance1}', not '{instance2}'")
def step_impl(context, instance1, instance2):
    for action, response in context.responses:
        tree = html.fromstring(response.content)
        assert tree.xpath(
            XPATH[action].format(context.instances[instance1].pk)
        ), "Can't see my instance"
        assert not tree.xpath(
            XPATH[action].format(context.instances[instance2].pk)
        ), "Shouldn't see not mine instance"


@then("The result is error code {status}")
def step_impl(context, status):
    for __, response in context.responses:
        assert response.status_code == int(status), response.status_code


@given("there is any {model}")
def step_imp(context, model):
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
def step_impl(context, action, model, app):
    pages = PAGES[action]
    args = [context.model_obj.pk] if hasattr(context, "model_obj") else []
    context.responses = []
    for action, method, needs_args in pages:
        response = getattr(context.test.client, method)(
            reverse(f"admin:{app}_{model}_{action}", args=args if needs_args else [])
        )
        context.responses.append((action, response))
