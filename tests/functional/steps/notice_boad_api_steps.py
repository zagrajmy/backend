from datetime import timedelta

from behave import given, then, when
from django.urls import reverse
from django.utils import timezone

from notice_board.models import Meeting
from tests.factories import GuildFactory, MeetingFactory, SphereFactory, UserFactory


@given("I am logged in as a user")
def step_impl(context):
    password = "s3cr3t"
    context.user = UserFactory()
    context.user.set_password(password)
    context.user.save()
    response = context.api_client.login(
        username=context.user.username, password=password
    )
    assert response


@given("there is a sphere")
def step_impl(context):
    context.sphere = SphereFactory()


@given("there is a guild I {belong} belong to")
def step_impl(context, belong):
    context.guild = GuildFactory()
    if belong == "do":
        context.guild.members.add(context.user)


@given("there is a meeting connected to my guild and sphere")
def step_impl(context):
    context.meeting = MeetingFactory(
        guild=context.guild,
        organizer=context.user,
        sphere=context.sphere,
    )


def set_values(data_list):
    data = {}
    for key, value in data_list:
        if value == "empty":
            data[key] = ""
        elif value[0] == "+":
            data[key] = (
                timezone.localtime(timezone.now()) + timedelta(days=int(value[1:]))
            ).isoformat()
        elif value[0] == "-":
            data[key] = (
                timezone.localtime(timezone.now()) - timedelta(days=int(value[1:]))
            ).isoformat()
        elif value == "user":
            data[key] = str(UserFactory().uuid)
        else:
            ValueError("Unsupported value!")
    return data


def _set_update_meeting_payload(context):
    context.payload = {
        "description": "Description of a meeting 121",
        "end_time": (
            timezone.localtime(timezone.now()) + timedelta(days=3)
        ).isoformat(),
        "location": "Arnoldborough",
        "meeting_url": "http://conrad-herrera.com/",
        "name": "Add could attention.",
        "participants_limit": 15,
        "publication_time": (
            timezone.localtime(timezone.now()) + timedelta(days=1)
        ).isoformat(),
        "slug": "add-could-attention",
        "start_time": (
            timezone.localtime(timezone.now()) + timedelta(days=2)
        ).isoformat(),
    }


def _set_create_meeting_payload(context):
    _set_update_meeting_payload(context)
    context.payload.update(
        {
            "guild": context.guild.id,
            "organizer": str(context.user.uuid),
            "sphere": context.sphere.id,
        }
    )


@when("I create a meeting")
def step_impl(context):
    _set_create_meeting_payload(context)
    context.response = context.api_client.post(
        reverse("v1:notice_board:meetings-list"), data=context.payload
    )


@when("I create a meeting with {data}")
def step_impl(context, data):
    data_dict = set_values([t.split(":") for t in data.split(",")])
    _set_create_meeting_payload(context)
    context.payload.update(data_dict)
    context.response = context.api_client.post(
        reverse("v1:notice_board:meetings-list"), data=context.payload
    )


def _update_meeting(context, data_dict):
    _set_update_meeting_payload(context)
    context.payload.update(data_dict)
    context.response = context.api_client.put(
        reverse("v1:notice_board:meetings-detail", kwargs={"pk": context.meeting.pk}),
        data=context.payload,
    )


@when("I update a meeting with {data}")
def step_impl(context, data):
    data_dict = set_values([t.split(":") for t in data.split(",")])
    _update_meeting(context, data_dict)


@when("I update a meeting setting {field} to {value}")
def step_impl(context, field, value):
    data_dict = set_values([[field, value]])
    _update_meeting(context, data_dict)


@then("I receive {status_code} response")
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code), context.response.json()


def dict_diff(dict1, dict2):
    if rdiff := set(dict2) - set(dict1):
        print(f"Keys missing in dict1: {rdiff}")
    for key, value in dict1.items():
        if value != dict2.get(key):
            print(f"Different values on key {key}: {value} vs {dict2.get(key)}")


@then("Response data is equals to the data I have sent")
def step_impl(context):
    response_data = dict(context.response.json())
    response_data.pop("id")
    context.payload["start_time"] = context.payload["start_time"] or None
    context.payload["end_time"] = context.payload["end_time"] or None
    context.payload["publication_time"] = context.payload["publication_time"] or None

    assert response_data == context.payload, dict_diff(response_data, context.payload)


@then('Response data contains error "{error}" for field {field}')
def step_impl(context, error, field):
    assert context.response.json()[field][0] == error, context.response.json()


@then("Meeting status is {status}")
def step_impl(context, status):
    assert Meeting.objects.get(id=context.response.json()["id"]).status == status


@given("there is a past meeting connected to my guild and sphere")
def step_impl(context):
    context.meeting = MeetingFactory(
        end_time=timezone.localtime(timezone.now()) - timedelta(days=2),
        guild=context.guild,
        organizer=context.user,
        publication_time=timezone.localtime(timezone.now()) - timedelta(days=6),
        sphere=context.sphere,
        start_time=timezone.localtime(timezone.now()) - timedelta(days=4),
    )


@when("I delete my meeting")
def step_impl(context):
    context.response = context.api_client.delete(
        reverse("v1:notice_board:meetings-detail", kwargs={"pk": context.meeting.pk})
    )


@then("Meeting doesn't exist")
def step_impl(context):
    meeting = Meeting.objects.filter(id=context.meeting.id)

    assert not meeting.exists()
