import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework.test import APIClient

from crowd.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create(api_client):
    res = api_client.post(
        reverse("v1:crowd:users-list"),
        data={
            "first_name": "Mszczuj",
            "last_name": "ze Skrzynna",
            "locale": "en-GB",
            "auth0_id": "test_token",
            "username": "panMszczuj",
        },
    )

    user = User.objects.first()
    assert str(user.uuid) == res.json().get("uuid")
    assert user.auth0_id == "test_token"
    assert user.first_name == res.json().get("first_name")
    assert user.last_name == "ze Skrzynna"
    assert user.locale == "en-GB"
    assert user.username == "panMszczuj"


@freeze_time("2020-07-04")
@pytest.mark.django_db
def test_get(api_client):
    user = User.objects.create(
        first_name="Mszczuj",
        last_name="ze Skrzynna",
        locale="en-GB",
        auth0_id="test_token",
        username="panMszczuj",
        email="mszczuj@grunwald.pl",
    )

    res = api_client.get(
        reverse("v1:crowd:users-detail", kwargs={"uuid": str(user.uuid)})
    )

    user_dict = res.json()
    assert len(user_dict.get("uuid", "")) == 36
    assert user_dict.get("auth0_id") == "test_token"
    assert user_dict.get("date_joined").startswith("2020-07-04")
    assert user_dict.get("first_name") == "Mszczuj"
    assert user_dict.get("last_name") == "ze Skrzynna"
    assert user_dict.get("locale") == "en-GB"
    assert user_dict.get("username") == "panMszczuj"
