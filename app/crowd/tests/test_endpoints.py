from django.urls import reverse

from freezegun import freeze_time
from rest_framework.test import APITestCase

from crowd.models import User


class TestCrowd(APITestCase):
    def setUp(self):
        self.users_url = reverse("v1:crowd:users-list")

    def test_create(self):
        res = self.client.post(
            self.users_url,
            data={
                "first_name": "Mszczuj",
                "last_name": "ze Skrzynna",
                "locale": "en-GB",
                "auth0_id": "test_token",
                "username": "panMszczuj",
            },
        )
        user = User.objects.first()
        self.assertEqual(user.first_name, res.json().get("first_name"))
        self.assertEqual(user.last_name, "ze Skrzynna")
        self.assertEqual(user.locale, "en-GB")
        self.assertEqual(user.auth0_id, "test_token")
        self.assertEqual(user.username, "panMszczuj")

    @freeze_time("2020-07-04")
    def test_get(self):
        user = User.objects.create(
            first_name="Mszczuj",
            last_name="ze Skrzynna",
            locale="en-GB",
            auth0_id="test_token",
            username="panMszczuj",
            email="mszczuj@grunwald.pl",
        )
        user_object_url = reverse(
            "v1:crowd:users-detail", kwargs={"uuid": str(user.uuid)}
        )
        res = self.client.get(user_object_url)
        user_dict = res.json()
        self.assertEqual("Mszczuj", user_dict.get("first_name"))
        self.assertEqual("ze Skrzynna", user_dict.get("last_name"))
        self.assertEqual("en-GB", user_dict.get("locale"))
        self.assertEqual("test_token", user_dict.get("auth0_id"))
        self.assertEqual("panMszczuj", user_dict.get("username"))
        self.assertTrue(user_dict.get("date_joined").startswith("2020-07-04"))
        self.assertEqual(36, len(user_dict.get("uuid", "")))
