from django.core.exceptions import ValidationError
from django.test import TestCase

from crowd.models import User


class UserTestCase(TestCase):
    def test_user_has_unique_uuid(self):
        user1 = User.objects.create(username="user1")
        user2 = User.objects.create(username="user2")

        self.assertNotEqual(user1.uuid, user2.uuid)

    def test_username_is_not_required(self):
        user1 = User(first_name="Maciek")

        self.assertIsNone(user1.clean())

    def test_username_is_not_unique(self):
        user1 = User.objects.create(username="", first_name="Maciek")
        user2 = User.objects.create(username="", first_name="Maciek")

        self.assertEqual(user1.username, user2.username)

    def test_username_or_first_name_should_be_provided(self):
        with self.assertRaisesRegex(ValidationError, "Missing username or first_name."):
            User().clean()

    def test_username_is_not_required_in_manager(self):
        user = User.objects.create_user(first_name="Maciek")

        self.assertEqual(user.first_name, "Maciek")
        self.assertEqual(user.username, "")

    def test_username_or_first_name_should_be_provided_in_manager(self):
        with self.assertRaisesRegex(ValidationError, "Missing username or first_name."):
            User.objects.create_user()

    def test_str(self):
        user = User(first_name="Maciek")

        self.assertEqual(str(user), "Maciek")

    def test_get_full_name_with_username(self):
        user = User(first_name="Maciek", last_name="Smith", username="drEvil")

        self.assertEqual(str(user), "Maciek Smith (drEvil)")
